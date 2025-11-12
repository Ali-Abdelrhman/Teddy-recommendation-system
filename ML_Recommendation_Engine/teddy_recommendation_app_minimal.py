#!/usr/bin/env python3
"""🧸 Teddy Recommendation System - Minimal Production Interface"""

import pickle, pandas as pd, numpy as np, gradio as gr, os, json, warnings, random, hashlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')

class RecommendationEngine:
    def __init__(self):
        self.model, self.is_loaded, self.catalog_data = None, False, {}
    
    def load_model(self, model_path: str) -> bool:
        try:
            with open(os.path.join(model_path, "metadata.json")) as f:
                self.model_type = json.load(f).get('best_model', 'Unknown')
            with open(os.path.join(model_path, "best_model.pkl"), "rb") as f:
                self.model = pickle.load(f)
            self._load_catalog()
            self.is_loaded = True
            return True
        except:
            return False
    
    def _load_catalog(self):
        try:
            with open("final_catalog_clean_urls.ndjson", 'r', encoding='utf-8') as f:
                for line in f:
                    item = json.loads(line.strip())
                    pid = str(item['id'])
                    self.catalog_data[pid] = {'image_url': item['images'][0].get('uri', '') if item.get('images') else '', 'uri': item.get('uri', '')}
        except: pass
    
    def get_recommendations(self, user_id: str, num_recs: int = 8):
        if not self.is_loaded: return {"error": "Model not loaded"}
        user_id = str(user_id).strip()
        
        if self.model['model_type'] == 'hybrid': return self._hybrid(user_id, num_recs)
        elif self.model['model_type'] == 'content_based': return self._content(user_id, num_recs)
        elif self.model['model_type'] == 'collaborative_filtering': return self._cf(user_id, num_recs)
        return {"error": "Unknown model type"}
    
    def _get_user_seed(self, user_id): return int(hashlib.md5(str(user_id).encode()).hexdigest()[:8], 16) % 100000
    def _get_user_prefs(self, user_id): h = hash(str(user_id)); c = (h % 100) / 100.0; return c, 1.0 - c
    
    def _content(self, user_id: str, num_recs: int):
        try:
            interactions = self.model['filtered_interaction_matrix']
            user_data = interactions[interactions['user_id'] == user_id]
            if user_data.empty: 
                print(f"🆕 Cold-start for user {user_id}")
                return self._cold_start(user_id, num_recs)
            
            products_df = self.model['products_df']
            user_products = set(user_data['product_id'])
            user_brands, user_categories = set(), set()
            
            for pid in user_products:
                if pid in self.model['product_id_to_idx']:
                    product = products_df.iloc[self.model['product_id_to_idx'][pid]]
                    user_brands.add(product['brand_main'])
                    user_categories.add(product['category_main'])
            
            profile = f"{' '.join(user_categories)} {' '.join(user_brands)}".strip()
            if not profile: 
                print(f"🆕 Cold-start for user {user_id} (no profile)")
                return self._cold_start(user_id, num_recs)
            
            print(f"📊 Content-based for user {user_id}")
            
            vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
            texts = [profile] + products_df['content_text'].tolist()
            tfidf_matrix = vectorizer.fit_transform(texts)
            similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            
            # Add personalization
            seed = self._get_user_seed(user_id)
            random.seed(seed)
            similarities += np.array([random.uniform(-0.1, 0.1) for _ in range(len(similarities))])
            
            recommendations = []
            for idx in np.argsort(similarities)[::-1][:num_recs]:
                product = products_df.iloc[idx]
                if product['product_id'] not in user_products:
                    rec = self._build_product_rec(product, product['product_id'])
                    rec.update({'score': float(similarities[idx]), 'model': 'Content-Based'})
                    recommendations.append(rec)
            return {'user_id': user_id, 'recommendations': recommendations, 'model_type': 'Content-Based'}
        except Exception as e:
            return {"error": f"Content error: {str(e)}"}
    
    def _cf(self, user_id: str, num_recs: int):
        if user_id not in self.model.get('user_to_idx', {}): 
            print(f"🆕 Cold-start for user {user_id}")
            return self._cold_start(user_id, num_recs)
        
        print(f"🤝 CF for user {user_id}")
        
        if 'brand_aware_popularity' in self.model:
            product_scores = list(self.model['brand_aware_popularity'].head(50).items())
        else: return self._cold_start(user_id, num_recs)
        
        recommendations = []
        for pid, score in product_scores[:num_recs]:
            if pid in self.model.get('product_metadata', {}):
                rec = self._enrich(self.model['product_metadata'][pid].copy(), pid)
                rec.update({'score': float(score), 'model': 'CF'})
                recommendations.append(rec)
        
        return {'user_id': user_id, 'recommendations': recommendations, 'model_type': 'CF'}
    
    def _hybrid(self, user_id: str, num_recs: int):
        print(f"🎯 Hybrid for user {user_id}")
        content_result = self._content(user_id, num_recs * 2)
        cf_result = self._cf(user_id, num_recs * 2)
        
        if 'error' in content_result and 'error' in cf_result: 
            print(f"🆕 Cold-start for user {user_id} (hybrid fallback)")
            return self._cold_start(user_id, num_recs)
        if 'error' in content_result: 
            print(f"🤝 CF only for user {user_id}")
            return cf_result
        if 'error' in cf_result: 
            print(f"📊 Content only for user {user_id}")
            return content_result
        
        # Simple combination - take half from each
        print(f"✅ Hybrid complete for user {user_id}")
        recommendations = content_result.get('recommendations', [])[:num_recs//2] + cf_result.get('recommendations', [])[:num_recs//2]
        return {'user_id': user_id, 'recommendations': recommendations[:num_recs], 'model_type': 'Hybrid'}
    
    def _cold_start(self, user_id: str, num_recs: int):
        try:
            print(f"❄️ Cold-start recommendations for user {user_id}")
            if 'brand_aware_popularity' in self.model:
                popular = list(self.model['brand_aware_popularity'].head(50).index)
            else:
                popular = list(self.model['interaction_matrix'].groupby('product_id')['weight'].sum().head(50).index)
            
            recommendations = []
            for pid in popular[:num_recs]:
                if pid in self.model.get('product_metadata', {}):
                    rec = self._enrich(self.model['product_metadata'][pid].copy(), pid)
                elif 'products_df' in self.model and pid in self.model['product_id_to_idx']:
                    product = self.model['products_df'].iloc[self.model['product_id_to_idx'][pid]]
                    rec = self._build_product_rec(product, pid)
                else: continue
                rec.update({'model': 'Cold Start', 'score': 1.0})
                recommendations.append(rec)
            
            return {'user_id': user_id, 'recommendations': recommendations, 'model_type': 'Cold Start'}
        except:
            return {"error": "Cold start failed"}
    

    
    def _build_product_rec(self, product, pid):
        rec = {'product_id': pid, 'title': product['title'], 'brand': product['brand_main'], 'category': product['category_main'], 'price': product['price']}
        return self._enrich(rec, pid)
    
    def _enrich(self, product_data, pid):
        if str(pid) in self.catalog_data: product_data.update(self.catalog_data[str(pid)])
        return product_data

def create_interface(engine):
    def get_recs(user_id, num_recs):
        if not engine.is_loaded: return '<h3>⚠️ Model Not Ready</h3>'
        if not user_id.strip(): return '<h3>❌ Enter User ID</h3>'
        
        result = engine.get_recommendations(user_id, max(1, min(int(num_recs or 8), 20)))
        if 'error' in result: return f'<h3>❌ {result["error"]}</h3>'
        
        recs = result['recommendations']
        if not recs: return '<h3>No recommendations</h3>'
        
        html = '<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px; text-align: center;"><h2>Recommendation Results</h2></div>'
        html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; margin: 20px 0;">'
        
        for i, rec in enumerate(recs, 1):
            image_url = rec.get('image_url', '')
            product_url = rec.get('uri', '')
            
            # Image with fallback (exact working approach)
            img_html = f"<img src='{image_url}' alt='Product' style='width: 150px; height: 150px; object-fit: cover; border-radius: 12px; border: 1px solid #555; margin: 0 auto; display: block;' />" if image_url else "<div style='width: 150px; height: 150px; background: #333; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #999; font-size: 14px; margin: 0 auto;'>No Image</div>"
            
            # Title with link
            if product_url:
                title_html = f"<a href='{product_url}' target='_blank' style='color: #3498db; text-decoration: none; font-weight: bold;'>{rec['title']}</a>"
                button_html = f"<a href='{product_url}' target='_blank' style='background: #3498db; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 14px; margin-top: 10px; display: inline-block;'>🔗 View Product</a>"
            else:
                title_html = f"<span style='color: #2c3e50; font-weight: bold;'>{rec['title']}</span>"
                button_html = ""
            
            html += f'''
            <div style="background: transparent; border: 1px solid #444; border-radius: 12px; padding: 20px;">
                <div style="display: flex; flex-direction: column; gap: 15px; height: 100%;">
                    <div style="text-align: center;">{img_html}</div>
                    <div style="text-align: center;">
                        <h3 style="margin: 0 0 10px 0; color: #3498db; font-size: 16px; font-weight: 600;">{i}. {title_html}</h3>
                        <div style="display: flex; flex-direction: column; gap: 8px; align-items: center;">
                            <span style="color: #e74c3c; font-weight: 500;">🏷️ {rec['brand']}</span>
                            <span style="color: #9b59b6; font-weight: 500;">📁 {rec['category']}</span>
                            {"<span style='color: #f39c12; font-weight: 500;'>👶 " + rec.get('age_group', '') + "</span>" if rec.get('age_group') else ""}
                            {"<span style='color: #e67e22; font-weight: 500;'>🎨 " + rec.get('color', '') + "</span>" if rec.get('color') else ""}
                            {"<span style='color: #27ae60; font-weight: 500;'>💰 " + str(round(rec.get('discount_percent', 0), 1)) + "% OFF</span>" if rec.get('discount_percent', 0) > 0 else ""}
                        </div>
                    </div>
                    <div style="margin-top: auto;">{button_html}</div>
                </div>
            </div>'''
        
        return html + '</div>'
    
    with gr.Blocks() as demo:
        gr.Markdown("# 🧸 Teddy Recommendations")
        user_input = gr.Textbox(label="User ID", placeholder="e.g., 1, 100001, NEW_USER")
        num_input = gr.Slider(1, 20, value=8, label="Count")
        btn = gr.Button("Get Recommendations")
        output = gr.HTML()
        btn.click(get_recs, [user_input, num_input], output)
    return demo

engine = RecommendationEngine()
models = [d for d in os.listdir("saved_models_production") if d.startswith("best_teddy_model_")]
if models: engine.load_model(os.path.join("saved_models_production", sorted(models)[-1]))
create_interface(engine).launch()