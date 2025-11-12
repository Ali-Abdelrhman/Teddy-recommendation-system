#!/usr/bin/env python3
"""Teddy Recommendation System - Production Interface"""

import pickle
import pandas as pd
import numpy as np
import gradio as gr
import os
import json
import warnings
warnings.filterwarnings('ignore')

class TeddyRecommendationEngine:
    def __init__(self):
        self.model = None
        self.preprocessors = None
        self.metadata = None
        self.is_loaded = False
        self.model_type = None
        
    def load_models(self, model_path):
        try:
            print(f"🔄 Loading best model from: {model_path}")
            
            with open(os.path.join(model_path, "metadata.json"), "r") as f:
                self.metadata = json.load(f)
            
            self.model_type = self.metadata.get('best_model', 'Unknown')
            print(f"🏆 Loading {self.model_type} model")
            
            with open(os.path.join(model_path, "preprocessors.pkl"), "rb") as f:
                self.preprocessors = pickle.load(f)
            
            with open(os.path.join(model_path, "best_model.pkl"), "rb") as f:
                self.model = pickle.load(f)
            
            self._enrich_product_metadata()
            self.is_loaded = True
            print("✅ Best model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.is_loaded = False
            return False
    
    def _enrich_product_metadata(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            catalog_file = os.path.join(script_dir, "final_catalog_clean_urls.ndjson")
            
            if not os.path.exists(catalog_file):
                print(f"⚠️ Catalog file not found")
                return
            
            catalog_data = {}
            with open(catalog_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        item = json.loads(line.strip())
                        product_id = str(item['id'])
                        image_url = item['images'][0].get('uri', '') if item.get('images') else ''
                        
                        # Enhanced metadata extraction with all new fields
                        catalog_data[product_id] = {
                            'image_url': image_url,
                            'uri': item.get('uri', ''),
                            'age_group': str(item.get('attributes', {}).get('age_group', {}).get('text', [''])[0] if item.get('attributes', {}).get('age_group', {}).get('text') else ''),
                            'color': str(item.get('attributes', {}).get('color', {}).get('text', [''])[0] if item.get('attributes', {}).get('color', {}).get('text') else ''),
                            'features': ' '.join(item.get('attributes', {}).get('features', {}).get('text', [])) if item.get('attributes', {}).get('features', {}).get('text') else '',
                            'tags': ' '.join(item.get('tags', [])) if item.get('tags') else '',
                            'availability': str(item.get('availability', 'UNKNOWN')),
                            'original_price': float(item.get('priceInfo', {}).get('originalPrice', 0))
                        }
                        
                        # Calculate discount percentage
                        price = float(item.get('priceInfo', {}).get('price', 0))
                        original_price = catalog_data[product_id]['original_price']
                        if original_price > 0 and price > 0:
                            catalog_data[product_id]['discount_percent'] = ((original_price - price) / original_price) * 100
                        else:
                            catalog_data[product_id]['discount_percent'] = 0.0
                    except:
                        continue
            
            if self.model['model_type'] == 'collaborative_filtering' and 'product_metadata' in self.model:
                for product_id, metadata in self.model['product_metadata'].items():
                    if str(product_id) in catalog_data:
                        metadata.update(catalog_data[str(product_id)])
                    else:
                        # Default enhanced fields for missing products
                        metadata.update({
                            'image_url': '', 'uri': '', 'age_group': '', 'color': '',
                            'features': '', 'tags': '', 'availability': 'UNKNOWN',
                            'original_price': 0.0, 'discount_percent': 0.0
                        })
            
            elif self.model['model_type'] in ['content_based', 'hybrid'] and 'products_df' in self.model:
                products_df = self.model['products_df']
                
                # Add enhanced field columns if they don't exist
                enhanced_fields = ['image_url', 'uri', 'age_group', 'color', 'features', 'tags', 'availability', 'original_price', 'discount_percent']
                for field in enhanced_fields:
                    if field not in products_df.columns:
                        products_df[field] = ''
                
                # Optimize metadata enrichment - use vectorized operations
                for field in enhanced_fields:
                    products_df[field] = products_df['product_id'].astype(str).apply(
                        lambda pid: catalog_data.get(pid, {}).get(field, '') if pid in catalog_data else ''
                    )
                
                if self.model['model_type'] == 'hybrid' and 'product_metadata' in self.model:
                    for product_id, metadata in self.model['product_metadata'].items():
                        if str(product_id) in catalog_data:
                            metadata.update(catalog_data[str(product_id)])
                        else:
                            # Default enhanced fields for missing products
                            metadata.update({
                                'image_url': '', 'uri': '', 'age_group': '', 'color': '',
                                'features': '', 'tags': '', 'availability': 'UNKNOWN',
                                'original_price': 0.0, 'discount_percent': 0.0
                            })
                            
        except Exception as e:
            print(f"⚠️ Error enriching metadata: {e}")
    
    def get_recommendations_for_user(self, user_id, num_recommendations=10):
        if not self.is_loaded:
            return {"error": "Models not loaded"}
        
        try:
            user_id = str(user_id).strip()
            
            if self.model['model_type'] == 'collaborative_filtering':
                return self._get_cf_recommendations(user_id, num_recommendations)
            elif self.model['model_type'] == 'content_based':
                return self._get_content_recommendations(user_id, num_recommendations)
            elif self.model['model_type'] == 'hybrid':
                return self._get_hybrid_recommendations(user_id, num_recommendations)
            else:
                return {"error": f"Unknown model type: {self.model['model_type']}"}
                
        except Exception as e:
            return {"error": f"Error generating recommendations: {str(e)}"}
    
    def _get_content_recommendations(self, user_id, num_recommendations):
        try:
            interaction_matrix = self.model['filtered_interaction_matrix']
            user_interactions = interaction_matrix[interaction_matrix['user_id'] == user_id]
            

            
            if user_interactions.empty:
                return self._get_cold_start_recommendations(num_recommendations, user_id)
            
            user_products = set(user_interactions['product_id'])
            user_brands = set()
            user_categories = set()
            
            products_df = self.model['products_df']
            product_id_to_idx = self.model['product_id_to_idx']
            
            for pid in user_products:
                if pid in product_id_to_idx:
                    idx = product_id_to_idx[pid]
                    product = products_df.iloc[idx]
                    user_brands.add(product['brand_main'])
                    user_categories.add(product['category_main'])
            
            user_profile_text = f"{' '.join(user_categories)} {' '.join(user_brands)}".strip()
            
            if not user_profile_text:
                return self._get_cold_start_recommendations(num_recommendations, user_id)
            
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            
            temp_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
            combined_texts = [user_profile_text] + products_df['content_text'].tolist()
            temp_matrix = temp_vectorizer.fit_transform(combined_texts)
            
            user_vector = temp_matrix[0:1]
            product_vectors = temp_matrix[1:]
            similarities = cosine_similarity(user_vector, product_vectors).flatten()
            
            # Add user-specific randomization to similarity scores
            import random
            import hashlib
            user_seed = int(hashlib.md5(str(user_id).encode()).hexdigest()[:8], 16) % 10000
            random.seed(user_seed)
            
            # Add significant user-specific noise to break identical patterns
            user_variations = np.array([random.uniform(-0.1, 0.1) for _ in range(len(similarities))])
            modified_similarities = similarities + user_variations
            
            recommendations = []
            used_brands = set()
            product_indices = np.argsort(modified_similarities)[::-1]
            
            print(f"🎯 CONTENT: User {user_id} - orig top sim: {similarities[product_indices[0]]:.4f}, modified: {modified_similarities[product_indices[0]]:.4f}")
            
            for idx in product_indices:
                if len(recommendations) >= num_recommendations:
                    break
                
                product = products_df.iloc[idx]
                product_id = product['product_id']
                
                if product_id in user_products:
                    continue
                
                brand = product['brand_main']
                if brand not in used_brands or len(used_brands) < num_recommendations // 2:
                    recommendations.append({
                        'product_id': product_id,
                        'title': product['title'],
                        'brand': brand,
                        'category': product['category_main'],
                        'price': product['price'],
                        'age_group': product.get('age_group', ''),
                        'color': product.get('color', ''),
                        'discount_percent': product.get('discount_percent', 0),
                        'availability': product.get('availability', 'UNKNOWN'),
                        'score': float(similarities[idx]),
                        'model': 'Content-Based',
                        'image_url': product.get('image_url', ''),
                        'uri': product.get('uri', '')
                    })
                    used_brands.add(brand)
            
            return {
                'user_id': user_id,
                'recommendations': recommendations,
                'model_type': 'Content-Based',
                'total_brands': len(used_brands)
            }
            
        except Exception as e:
            return {"error": f"Content-based error: {str(e)}"}
    
    def _get_cf_recommendations(self, user_id, num_recommendations):
        try:

            
            if user_id not in self.model['user_to_idx']:
                return self._get_cold_start_recommendations(num_recommendations, user_id)
            
            user_idx = self.model['user_to_idx'][user_id]
            user_interactions = set(self.model['filtered_interaction_matrix'][
                self.model['filtered_interaction_matrix']['user_id'] == user_id]['product_id'])
            
            if hasattr(self.model, 'U') and self.model.get('U') is not None:
                user_profile = self.model['U'][user_idx, :]
                scores = np.dot(user_profile, self.model['sigma'].reshape(-1, 1) * self.model['Vt']).flatten()
                product_scores = list(zip(self.model['unique_products'], scores))
            else:
                product_scores = [(pid, score) for pid, score in self.model['brand_aware_popularity'].items()]
            
            # Add user-specific randomization to CF scores
            import random
            import hashlib
            user_seed = int(hashlib.md5(str(user_id).encode()).hexdigest()[:8], 16) % 10000
            random.seed(user_seed)
            
            # Apply user-specific variations to break identical rankings
            varied_scores = []
            for product_id, score in product_scores:
                variation = random.uniform(-0.2, 0.2)  # Larger variation for CF
                varied_scores.append((product_id, score + variation))
            
            recommendations = []
            used_brands = set()
            product_metadata = self.model['product_metadata']
            
            sorted_scores = sorted(varied_scores, key=lambda x: x[1], reverse=True)
            print(f"🎯 CF: User {user_id} - top 3 products: {[s[0] for s in sorted_scores[:3]]}")
            
            for product_id, score in sorted_scores:
                if len(recommendations) >= num_recommendations:
                    break
                
                if product_id in user_interactions or product_id not in product_metadata:
                    continue
                
                metadata = product_metadata[product_id]
                brand = metadata['brand']
                
                if brand not in used_brands or len(used_brands) < num_recommendations // 2:
                    recommendations.append({
                        'product_id': product_id,
                        'title': metadata['title'],
                        'brand': brand,
                        'category': metadata['category'],
                        'price': metadata['price'],
                        'age_group': metadata.get('age_group', ''),
                        'color': metadata.get('color', ''),
                        'discount_percent': metadata.get('discount_percent', 0),
                        'availability': metadata.get('availability', 'UNKNOWN'),
                        'score': float(score),
                        'model': 'Collaborative Filtering',
                        'image_url': metadata.get('image_url', ''),
                        'uri': metadata.get('uri', '')
                    })
                    used_brands.add(brand)
            
            return {
                'user_id': user_id,
                'recommendations': recommendations,
                'model_type': 'Collaborative Filtering',
                'total_brands': len(used_brands)
            }
            
        except Exception as e:
            return {"error": f"Collaborative filtering error: {str(e)}"}
    
    def _get_hybrid_recommendations(self, user_id, num_recommendations):
        try:
            print(f"🎯 HYBRID: Starting for user {user_id}")
            
            if 'products_df' in self.model and 'interaction_matrix' in self.model:
                content_result = self._get_content_recommendations(user_id, num_recommendations * 3)
                print(f"🎯 HYBRID: Content got {len(content_result.get('recommendations', []))} recs")
            else:
                content_result = {"error": "Missing content components"}
            
            if 'user_to_idx' in self.model and 'product_metadata' in self.model:
                cf_result = self._get_cf_recommendations(user_id, num_recommendations * 3)
                print(f"🎯 HYBRID: CF got {len(cf_result.get('recommendations', []))} recs")
            else:
                cf_result = {"error": "Missing CF components"}
            
            if 'error' in content_result and 'error' in cf_result:
                print(f"🎯 HYBRID: Both failed, using cold-start for {user_id}")
                return self._get_cold_start_recommendations(num_recommendations, user_id)
            elif 'error' in content_result:
                print(f"🎯 HYBRID: Content failed, using CF only for {user_id}")
                cf_result['model_type'] = 'Hybrid (CF Only)'
                return cf_result
            elif 'error' in cf_result:
                print(f"🎯 HYBRID: CF failed, using content only for {user_id}")
                content_result['model_type'] = 'Hybrid (Content Only)'
                return content_result
            
            content_recs = content_result.get('recommendations', [])
            cf_recs = cf_result.get('recommendations', [])
            
            combined_scores = {}
            product_info = {}
            
            content_weight = self.model.get('content_weight', 0.65)
            cf_weight = self.model.get('cf_weight', 0.35)
            
            print(f"🎯 HYBRID: Combining {len(content_recs)} content + {len(cf_recs)} CF recs")
            
            # AGGRESSIVE USER-SPECIFIC DIVERSIFICATION
            import random
            import hashlib
            import numpy as np
            
            user_seed = int(hashlib.md5(str(user_id).encode()).hexdigest()[:8], 16) % 10000
            random.seed(user_seed)
            np.random.seed(user_seed)
            
            # Create user-specific preference shifts
            user_hash = hash(str(user_id))
            content_preference = (user_hash % 100) / 100.0  # 0-1 content preference
            cf_preference = 1.0 - content_preference
            
            print(f"🎯 HYBRID: User {user_id} - content pref: {content_preference:.3f}, CF pref: {cf_preference:.3f}")
            
            # Aggressive shuffling and selection based on user preference
            content_shuffled = content_recs.copy()
            cf_shuffled = cf_recs.copy()
            np.random.shuffle(content_shuffled)
            np.random.shuffle(cf_shuffled)
            
            # Dynamic selection based on user preference (30-90% of each)
            content_take = int(len(content_shuffled) * (0.3 + content_preference * 0.6))
            cf_take = int(len(cf_shuffled) * (0.3 + cf_preference * 0.6))
            
            content_selected = content_shuffled[:content_take]
            cf_selected = cf_shuffled[:cf_take]
            
            print(f"🎯 HYBRID: Taking {content_take}/{len(content_recs)} content, {cf_take}/{len(cf_recs)} CF")
            
            # Apply strong user-specific scoring variations
            for rec in content_selected:
                pid = rec['product_id']
                # Very strong variation + user preference boost
                variation = (random.random() - 0.5) * 0.5  # ±0.25 variation
                preference_boost = content_preference * 0.3  # Up to +0.3 boost
                combined_scores[pid] = (content_weight * rec['score']) + variation + preference_boost
                product_info[pid] = rec
            
            for rec in cf_selected:
                pid = rec['product_id']
                variation = (random.random() - 0.5) * 0.5  # ±0.25 variation  
                preference_boost = cf_preference * 0.3  # Up to +0.3 boost
                score = (cf_weight * rec['score']) + variation + preference_boost
                combined_scores[pid] = combined_scores.get(pid, 0) + score
                if pid not in product_info:
                    product_info[pid] = rec
            
            sorted_products = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
            recommendations = []
            used_brands = set()
            
            for pid, score in sorted_products:
                if len(recommendations) >= num_recommendations:
                    break
                
                rec = product_info[pid]
                brand = rec['brand']
                
                if brand not in used_brands or len(used_brands) < num_recommendations // 2:
                    rec_copy = rec.copy()
                    rec_copy['score'] = float(score)
                    rec_copy['model'] = 'Hybrid'
                    recommendations.append(rec_copy)
                    used_brands.add(brand)
            
            return {
                'user_id': user_id,
                'recommendations': recommendations,
                'model_type': 'Hybrid',
                'total_brands': len(used_brands)
            }
            
        except Exception as e:
            return {"error": f"Hybrid error: {str(e)}"}
    
    def _get_cold_start_recommendations(self, num_recommendations, user_id=None):
        try:
            import random
            import hashlib
            
            # Create user-specific randomization seed with more variation
            if user_id and user_id != 'NEW_USER':
                # Use hash of user_id for consistent but different results per user
                hash_obj = hashlib.md5(str(user_id).encode())
                seed = int(hash_obj.hexdigest()[:8], 16) % 100000
                random.seed(seed)
                print(f"🎯 Cold-start for user {user_id} with seed {seed}")
            else:
                # For truly new users, use time-based randomization
                import time
                seed = int(time.time() * 1000) % 100000
                random.seed(seed)
                print(f"🎯 Cold-start for NEW_USER with seed {seed}")
            
            if self.model['model_type'] == 'collaborative_filtering' and 'brand_aware_popularity' in self.model:
                # Get broader range of products for user-specific selection
                all_popular = list(self.model['brand_aware_popularity'].head(min(150, len(self.model['brand_aware_popularity']))).index)
                
                # Use user-specific segment selection for maximum diversity
                if user_id:
                    user_numeric = sum(ord(c) for c in str(user_id)) % 10000
                    interval = max(2, (user_numeric % 8) + 2)  # Intervals 2-9
                    offset = user_numeric % min(50, len(all_popular))
                    
                    # Divide products into segments and select from each
                    popular_products = []
                    segments = 5
                    segment_size = len(all_popular) // segments
                    
                    for seg in range(segments):
                        start_idx = (seg * segment_size + offset + user_numeric * (seg + 1)) % len(all_popular)
                        for i in range(num_recommendations):
                            if len(popular_products) >= num_recommendations * 3:
                                break
                            idx = (start_idx + i * interval) % len(all_popular)
                            if all_popular[idx] not in popular_products:
                                popular_products.append(all_popular[idx])
                else:
                    random.shuffle(all_popular)
                    popular_products = all_popular[:num_recommendations * 3]
                
                print(f"🎯 CF COLD-START: User {user_id} -> numeric={user_numeric if user_id else 'N/A'}, selected {len(popular_products)} products from {len(all_popular)} available")
                if user_id and len(popular_products) > 0:
                    print(f"   First few products: {popular_products[:3]}")
                product_metadata = self.model['product_metadata']
                
                recommendations = []
                used_brands = set()
                
                for product_id in popular_products:
                    if len(recommendations) >= num_recommendations:
                        break
                    
                    if product_id in product_metadata:
                        metadata = product_metadata[product_id]
                        brand = metadata['brand']
                        
                        if brand not in used_brands:
                            recommendations.append({
                                'product_id': product_id,
                                'title': metadata['title'],
                                'brand': brand,
                                'category': metadata['category'],
                                'price': metadata['price'],
                                'age_group': metadata.get('age_group', ''),
                                'color': metadata.get('color', ''),
                                'discount_percent': metadata.get('discount_percent', 0),
                                'availability': metadata.get('availability', 'UNKNOWN'),
                                'score': 1.0,
                                'model': f'Cold Start ({user_id[:8] if user_id else "New"})',
                                'image_url': metadata.get('image_url', ''),
                                'uri': metadata.get('uri', '')
                            })
                            used_brands.add(brand)
                
                return {'user_id': 'NEW_USER', 'recommendations': recommendations, 'model_type': 'Cold Start', 'total_brands': len(used_brands)}
            
            elif self.model['model_type'] in ['content_based', 'hybrid']:
                interaction_matrix = self.model['interaction_matrix']
                popular_products = interaction_matrix.groupby('product_id')['weight'].sum().sort_values(ascending=False)
                products_df = self.model['products_df']
                product_id_to_idx = self.model['product_id_to_idx']
                
                # Get larger pool and create truly user-specific diverse selection
                popular_list = list(popular_products.head(min(300, len(popular_products))).items())
                
                # Use user ID to create completely different product selections
                selected_products = []
                if user_id:
                    # Convert user_id to numeric value for consistent selection
                    user_numeric = sum(ord(c) for c in str(user_id)) % 10000
                    
                    # Create user-specific intervals for different product ranges
                    interval = max(3, (user_numeric % 12) + 2)  # Intervals 2-13
                    offset = user_numeric % min(100, len(popular_list))  # Starting offset
                    
                    # Select products from different segments of the popularity list
                    segments = 4  # Divide into segments
                    segment_size = len(popular_list) // segments
                    
                    for seg in range(segments):
                        start_idx = (seg * segment_size + offset + user_numeric * seg) % len(popular_list)
                        for i in range(num_recommendations):
                            if len(selected_products) >= num_recommendations * 2:
                                break
                            idx = (start_idx + i * interval) % len(popular_list)
                            if popular_list[idx] not in selected_products:
                                selected_products.append(popular_list[idx])
                else:
                    random.shuffle(popular_list)
                    selected_products = popular_list[:num_recommendations * 2]
                
                print(f"🎯 HYBRID COLD-START: User {user_id} -> numeric={user_numeric if user_id else 'N/A'}, selected {len(selected_products)} products from {len(popular_list)} available")
                if user_id and len(selected_products) > 0:
                    print(f"   First few products: {[p[0] for p in selected_products[:3]]}")
                
                recommendations = []
                used_brands = set()
                
                for product_id, weight in selected_products:
                    if len(recommendations) >= num_recommendations:
                        break
                    
                    if product_id in product_id_to_idx:
                        idx = product_id_to_idx[product_id]
                        product = products_df.iloc[idx]
                        brand = product['brand_main']
                        
                        if brand not in used_brands:
                            recommendations.append({
                                'product_id': product_id,
                                'title': product['title'],
                                'brand': brand,
                                'category': product['category_main'],
                                'price': product['price'],
                                'age_group': product.get('age_group', ''),
                                'color': product.get('color', ''),
                                'discount_percent': product.get('discount_percent', 0),
                                'availability': product.get('availability', 'UNKNOWN'),
                                'score': 1.0,
                                'model': 'Cold Start',
                                'image_url': product.get('image_url', ''),
                                'uri': product.get('uri', '')
                            })
                            used_brands.add(brand)
                
                return {'user_id': 'NEW_USER', 'recommendations': recommendations, 'model_type': 'Cold Start', 'total_brands': len(used_brands)}
            
            return {"error": "No cold start data available"}
            
        except Exception as e:
            return {"error": f"Cold start error: {str(e)}"}
    
    def get_user_list(self):
        if not self.is_loaded:
            return []
        
        try:
            if self.model['model_type'] == 'collaborative_filtering':
                users = list(self.model['user_to_idx'].keys())
            elif self.model['model_type'] in ['content_based', 'hybrid']:
                users = list(self.model['interaction_matrix']['user_id'].unique())
            else:
                return []
                
            return sorted(users)[:100]
        except Exception as e:
            print(f"⚠️ Error getting user list: {e}")
            return []

# Initialize the recommendation engine
recommender = TeddyRecommendationEngine()

def load_models_interface():
    try:
        model_base_dir = "saved_models_production"
        
        if not os.path.exists(model_base_dir):
            return "❌ No saved models found"
        
        best_model_dirs = [d for d in os.listdir(model_base_dir) if d.startswith("best_teddy_model_")]
        
        if best_model_dirs:
            latest_model = sorted(best_model_dirs)[-1]
        else:
            return "❌ No best model directories found"
        
        model_path = os.path.join(model_base_dir, latest_model)
        
        required_files = ["metadata.json", "preprocessors.pkl", "best_model.pkl"]
        missing_files = [f for f in required_files if not os.path.exists(os.path.join(model_path, f))]
        
        if missing_files:
            return f"❌ Missing model files: {missing_files}"
        
        if recommender.load_models(model_path):
            return f"✅ Best model loaded successfully!\n📂 From: {latest_model}\n🎯 Model type: {recommender.model_type}"
        else:
            return "❌ Failed to load best model"
            
    except Exception as e:
        return f"❌ Error loading models: {str(e)}"

def get_recommendations_interface(user_id, num_recs):
    if not recommender.is_loaded:
        return '<div style="background: linear-gradient(135deg, #ff7b7b 0%, #ffaa7b 100%); padding: 30px; border-radius: 15px; color: white; text-align: center;"><h2>⚠️ Model Not Ready</h2><p>Please wait and try again</p></div>'
    
    if not user_id.strip():
        return '<div style="background: linear-gradient(135deg, #ff7b7b 0%, #ffaa7b 100%); padding: 20px; border-radius: 15px; color: white; text-align: center;"><h3>❌ Please enter a valid User ID</h3></div>'
    
    try:
        num_recs = max(1, min(int(num_recs), 20))
    except:
        num_recs = 8
    
    result = recommender.get_recommendations_for_user(user_id, num_recs)
    
    if 'error' in result:
        return f'<div style="background: linear-gradient(135deg, #ff7b7b 0%, #ffaa7b 100%); padding: 20px; border-radius: 15px; color: white; text-align: center;"><h3>❌ {result["error"]}</h3></div>'
    
    recommendations = result['recommendations']
    
    if not recommendations:
        return '<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white; text-align: center;"><h3>No recommendations found</h3></div>'
    
    output = '<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px; text-align: center;"><h2>Recommendation Results</h2></div><div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; margin: 20px 0;">'
    
    for i, rec in enumerate(recommendations, 1):
        image_url = rec.get('image_url', '')
        product_url = rec.get('uri', '')
        
        image_html = f"<img src='{image_url}' alt='Product' style='width: 150px; height: 150px; object-fit: cover; border-radius: 12px; border: 1px solid #555; margin: 0 auto; display: block;' />" if image_url else "<div style='width: 150px; height: 150px; background: #333; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #999; font-size: 14px; margin: 0 auto;'>No Image</div>"
        
        title_html = f"<a href='{product_url}' target='_blank' style='color: #3498db; text-decoration: none;'>{rec['title']}</a>" if product_url else rec['title']
        
        button_html = f"<a href='{product_url}' target='_blank' style='background: #3498db; color: white; padding: 12px 20px; border-radius: 8px; text-decoration: none; font-size: 16px; display: block; text-align: center; font-weight: 500;'><span style='font-size: 1.2em;'>🔗</span> View Product</a>" if product_url else ""
        
        output += f'''
<div style="background: transparent; border: 1px solid #444; border-radius: 12px; padding: 20px;">
    <div style="display: flex; flex-direction: column; gap: 15px; height: 100%;">
        <div style="text-align: center;">{image_html}</div>
        <div style="text-align: center;">
            <h3 style="margin: 0 0 10px 0; color: #3498db; font-size: 16px; font-weight: 600;">{i}. {title_html}</h3>
            <div style="display: flex; flex-direction: column; gap: 8px; align-items: center;">
                <span style="color: #e74c3c; font-weight: 500;"><span style='font-size: 1.2em;'>🏷️</span> {rec['brand']}</span>
                <span style="color: #9b59b6; font-weight: 500;"><span style='font-size: 1.2em;'>📁</span> {rec['category']}</span>
                {"<span style='color: #f39c12; font-weight: 500;'><span style='font-size: 1.2em;'>👶</span> " + rec.get('age_group', '') + "</span>" if rec.get('age_group') else ""}
                {"<span style='color: #e67e22; font-weight: 500;'><span style='font-size: 1.2em;'>🎨</span> " + rec.get('color', '') + "</span>" if rec.get('color') else ""}
                {"<span style='color: #27ae60; font-weight: 500;'><span style='font-size: 1.2em;'>💰</span> " + str(round(rec.get('discount_percent', 0), 1)) + "% OFF</span>" if rec.get('discount_percent', 0) > 0 else ""}
            </div>
        </div>
        <div style="margin-top: auto;">{button_html}</div>
    </div>
</div>'''
    
    output += "</div>"
    return output

def get_sample_users():
    users = recommender.get_user_list()
    return f"📋 **Sample Users:** {', '.join(users[:10])}" if users else "Load models first"

def create_gradio_interface():
    with gr.Blocks(title="Teddy Recommendation System", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# <div align='center'><span style='font-size: 3em;'>🧸</span> Teddy Recommendation System</div>")
        
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Row():
                    user_id_input = gr.Textbox(label="User ID", placeholder="Enter visitor ID (e.g., 2170)", value="")
                    num_recs_input = gr.Slider(minimum=1, maximum=20, value=8, step=1, label="Number of Recommendations")
                
                recommend_btn = gr.Button("🚀 Get Recommendations" if recommender.is_loaded else "⏳ Loading Model...", variant="primary", interactive=recommender.is_loaded, size="lg")
        
        gr.Markdown("---")
        recommendations_output = gr.HTML(label="Recommendations")
        
        recommend_btn.click(fn=get_recommendations_interface, inputs=[user_id_input, num_recs_input], outputs=recommendations_output)
    
    return demo

if __name__ == "__main__":
    print("🔄 Auto-loading best model...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_base_dir = os.path.join(script_dir, "saved_models_production")
    
    if os.path.exists(model_base_dir):
        best_model_dirs = [d for d in os.listdir(model_base_dir) if d.startswith("best_teddy_model_")]
        
        if best_model_dirs:
            latest_model = sorted(best_model_dirs)[-1]
            model_path = os.path.join(model_base_dir, latest_model)
            
            if recommender.load_models(model_path):
                print(f"✅ Best model auto-loaded: {recommender.model_type}")
            else:
                print("❌ Failed to auto-load models")
        else:
            print("❌ No best model directories found")
    else:
        print("❌ Model directory not found")
    
    demo = create_gradio_interface()
    
    import random
    port = random.randint(7860, 7890)
    
    if recommender.is_loaded:
        print(f"🌐 Launching locally on port {port}")
        demo.launch(share=False, server_name="127.0.0.1", server_port=port, show_error=True)
    else:
        print(f"⚠️ Launching locally on port {port}")
        demo.launch(share=False, server_name="127.0.0.1", server_port=port, show_error=True)