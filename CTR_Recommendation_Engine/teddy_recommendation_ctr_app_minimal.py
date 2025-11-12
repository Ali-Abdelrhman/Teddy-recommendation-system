#!/usr/bin/env python3
"""Minimal Teddy Recommendation System"""

import pickle
import gradio as gr
import os
import json
import uuid
import random
import hashlib

class SimpleTracker:
    def __init__(self):
        self.count = 0
        
    def log(self):
        self.count += 1

class RecommendationEngine:
    def __init__(self):
        self.model = None
        self.is_loaded = False
        self.tracker = SimpleTracker()
        
    def load_model(self, model_path):
        try:
            with open(os.path.join(model_path, "best_model.pkl"), "rb") as f:
                self.model = pickle.load(f)
            
            self._enrich_product_images()
            self.is_loaded = True
            print(f"✅ Model loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _enrich_product_images(self):
        """Add image URLs to product metadata"""
        try:
            catalog_file = os.path.join(os.path.dirname(__file__), "final_catalog_clean_urls.ndjson")
            if not os.path.exists(catalog_file):
                return
            
            image_data = {}
            with open(catalog_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        item = json.loads(line.strip())
                        product_id = str(item['id'])
                        image_url = item['images'][0].get('uri', '') if item.get('images') else ''
                        if image_url:
                            image_data[product_id] = image_url
                    except:
                        continue
            
            # Add images to metadata
            if 'product_metadata' in self.model:
                for product_id, metadata in self.model['product_metadata'].items():
                    metadata['image_url'] = image_data.get(str(product_id), '')
                        
        except Exception as e:
            print(f"⚠️ Error enriching images: {e}")
    
    def get_recommendations(self, user_id, num_recommendations=8):
        if not self.is_loaded:
            return {"error": "Model not loaded"}
        
        try:
            user_id = str(user_id).strip()
            
            # Get recommendations based on model type
            if self.model.get('model_type') == 'collaborative_filtering':
                result = self._get_cf_recommendations(user_id, num_recommendations)
            else:
                result = self._get_cold_start_recommendations(num_recommendations, user_id)
            
            # Add display IDs and log
            for rec in result.get('recommendations', []):
                rec['display_id'] = str(uuid.uuid4())
                self.tracker.log()
            
            print(f"🎯 User: {user_id} | Generated: {len(result.get('recommendations', []))} recommendations")
            return result
                
        except Exception as e:
            return {"error": str(e)}
    
    def simulate_click(self, display_id, product_id):
        self.tracker.log()
        print(f"👆 CLICK: {product_id}")
    
    def _get_cf_recommendations(self, user_id, num_recommendations):
        try:
            if user_id not in self.model.get('user_to_idx', {}):
                return self._get_cold_start_recommendations(num_recommendations, user_id)
            
            # Use popularity scores with user randomization
            product_scores = [(pid, score) for pid, score in self.model['brand_aware_popularity'].items()]
            
            user_seed = int(hashlib.md5(str(user_id).encode()).hexdigest()[:8], 16) % 10000
            random.seed(user_seed)
            
            # Get recommendations
            recommendations = []
            product_metadata = self.model.get('product_metadata', {})
            
            for product_id, score in sorted(product_scores, key=lambda x: x[1], reverse=True):
                if len(recommendations) >= num_recommendations:
                    break
                
                if product_id in product_metadata:
                    metadata = product_metadata[product_id]
                    recommendations.append({
                        'product_id': product_id,
                        'title': metadata.get('title', 'Unknown Product'),
                        'brand': metadata.get('brand', 'Unknown'),
                        'price': metadata.get('price', 0),
                        'image_url': metadata.get('image_url', ''),
                        'score': float(score)
                    })
            
            return {
                'user_id': user_id,
                'recommendations': recommendations,
                'model_type': 'Collaborative Filtering'
            }
            
        except Exception as e:
            return {"error": f"CF error: {str(e)}"}
    

    
    def _get_cold_start_recommendations(self, num_recommendations, user_id=None):
        try:
            # Use popularity data if available
            if 'brand_aware_popularity' in self.model and 'product_metadata' in self.model:
                popularity_data = self.model['brand_aware_popularity']
                all_popular = list(popularity_data.keys())[:50] if isinstance(popularity_data, dict) else list(popularity_data.head(50).index)
                
                random.shuffle(all_popular)
                product_metadata = self.model['product_metadata']
                recommendations = []
                
                for product_id in all_popular:
                    if len(recommendations) >= num_recommendations:
                        break
                    
                    if product_id in product_metadata:
                        metadata = product_metadata[product_id]
                        recommendations.append({
                            'product_id': product_id,
                            'title': metadata.get('title', 'Teddy Bear'),
                            'brand': metadata.get('brand', 'Unknown'),
                            'price': metadata.get('price', 19.99),
                            'image_url': metadata.get('image_url', ''),
                            'score': 1.0
                        })
                
                if recommendations:
                    return {
                        'user_id': user_id or 'NEW_USER',
                        'recommendations': recommendations,
                        'model_type': 'Cold Start'
                    }
            
            # Fallback dummy data
            return {
                'user_id': user_id or 'NEW_USER',
                'recommendations': [{
                    'product_id': f'dummy_{i}',
                    'title': f'Teddy Bear {i+1}',
                    'brand': f'Brand {chr(65+i)}',
                    'price': 19.99 + i * 5,
                    'image_url': '',
                    'score': 1.0
                } for i in range(num_recommendations)],
                'model_type': 'Cold Start'
            }
            
        except Exception as e:
            return {"error": f"Cold start error: {str(e)}"}

# Initialize engine
recommender = RecommendationEngine()

def get_recommendations_interface(user_id, num_recs):
    if not recommender.is_loaded:
        return '<div style="background: #ff6b6b; padding: 20px; border-radius: 10px; color: white; text-align: center;"><h3>⚠️ Model Not Ready</h3></div>'
    
    if not user_id.strip():
        return '<div style="background: #ff6b6b; padding: 20px; border-radius: 10px; color: white; text-align: center;"><h3>❌ Please enter a User ID</h3></div>'
    
    try:
        num_recs = max(1, min(int(num_recs), 12))
    except:
        num_recs = 8
    
    result = recommender.get_recommendations(user_id, num_recs)
    
    # Auto-simulate clicks for learning
    if 'recommendations' in result and len(result['recommendations']) > 0:
        for i, rec in enumerate(result['recommendations'][:2]):
            if 'display_id' in rec:
                recommender.simulate_click(rec['display_id'], rec['product_id'])
    
    if 'error' in result:
        return f'<div style="background: #ff6b6b; padding: 20px; border-radius: 10px; color: white; text-align: center;"><h3>❌ {result["error"]}</h3></div>'
    
    recommendations = result['recommendations']
    
    if not recommendations:
        return '<div style="background: #4ecdc4; padding: 20px; border-radius: 10px; color: white; text-align: center;"><h3>No recommendations found</h3></div>'
    
    # Minimal card design with images
    output = '<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; color: white; margin-bottom: 15px; text-align: center;"><h2>🧸 Recommendations</h2></div>'
    output += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 15px 0;">'
    
    for i, rec in enumerate(recommendations, 1):
        image_url = rec.get('image_url', '')
        
        # Create image element or placeholder
        if image_url:
            image_html = f'''
            <div style="text-align: center; margin-bottom: 10px;">
                <img src="{image_url}" alt="Product Image" style="width: 120px; height: 120px; object-fit: cover; border-radius: 8px; border: 2px solid #eee;" />
            </div>'''
        else:
            image_html = f'''
            <div style="text-align: center; margin-bottom: 10px;">
                <div style="width: 120px; height: 120px; background: #f0f0f0; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin: 0 auto; border: 2px solid #eee;">
                    <span style="color: #999; font-size: 12px;">🧸<br>No Image</span>
                </div>
            </div>'''
        
        output += f'''
<div style="background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
    {image_html}
    <h3 style="margin: 0 0 5px 0; color: #333; font-size: 14px;">{i}. {rec['title'][:50]}...</h3>
    <p style="margin: 0; color: #666; font-size: 11px;">{rec.get('brand', 'Unknown Brand')}</p>
</div>'''
    
    output += "</div>"
    return output

def create_gradio_interface():
    with gr.Blocks(title="Teddy Recommendation System", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# <div align='center'>🧸 Teddy Recommendation System</div>")
        
        with gr.Row():
            user_id_input = gr.Textbox(label="User ID", placeholder="Enter user ID (e.g., 2170)", value="")
            num_recs_input = gr.Slider(minimum=4, maximum=12, value=8, step=1, label="Number of Recommendations")
        
        recommend_btn = gr.Button("🚀 Get Recommendations", variant="primary", size="lg")
        recommendations_output = gr.HTML(label="Recommendations")
        
        recommend_btn.click(fn=get_recommendations_interface, inputs=[user_id_input, num_recs_input], outputs=recommendations_output)
    
    return demo

if __name__ == "__main__":
    print("🧸 Starting Teddy Recommendation System...")
    
    # Auto-load model
    model_dir = os.path.join(os.path.dirname(__file__), "saved_models_production")
    
    if os.path.exists(model_dir):
        models = [d for d in os.listdir(model_dir) if d.startswith("best_teddy_model_")]
        if models:
            model_path = os.path.join(model_dir, sorted(models)[-1])
            recommender.load_model(model_path)
    
    demo = create_gradio_interface()
    print("🌐 Launching on http://localhost:7860")
    demo.launch(share=False, server_name="127.0.0.1", server_port=7860, show_error=True)