import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from . import models, database
from implicit.als import AlternatingLeastSquares


class ALSRecommender:
    def __init__(self, factors: int = 50, regularization: float = 0.01, iterations: int = 15):
        self.model = AlternatingLeastSquares(
            factors=factors,
            regularization=regularization,
            iterations=iterations,
        )
        self.user_id_mapping = {}
        self.item_id_mapping = {}
        self.user_index_mapping = {}
        self.item_index_mapping = {}
        self.user_items_matrix = None

    def train(self):
        session = database.SessionLocal()
        try:
            ratings_data = session.query(models.Rating).all()
            if not ratings_data:
                print("No ratings data found; skipping fit.")
                return

            user_ids = sorted({r.user_id for r in ratings_data})
            item_ids = sorted({r.movie_id for r in ratings_data})
            self.user_id_mapping = {uid: idx for idx, uid in enumerate(user_ids)}
            self.item_id_mapping = {iid: idx for idx, iid in enumerate(item_ids)}
            self.user_index_mapping = {idx: uid for uid, idx in self.user_id_mapping.items()}
            self.item_index_mapping = {idx: iid for iid, idx in self.item_id_mapping.items()}

            rows, cols, data = [], [], []
            for r in ratings_data:
                rows.append(self.user_id_mapping[r.user_id])
                cols.append(self.item_id_mapping[r.movie_id])
                data.append(float(r.rating))

            self.user_items_matrix = csr_matrix(
                coo_matrix((data, (rows, cols)), shape=(len(user_ids), len(item_ids)))
            )

            self.model.fit(self.user_items_matrix)
            print(f"ALS model trained with {len(user_ids)} users and {len(item_ids)} items.")
        finally:
            session.close()

    def recommend_for_user(self, user_id: int, N: int = 10):
        if self.user_items_matrix is None:
            raise RuntimeError("Model has not been trained yet.")

        if user_id not in self.user_id_mapping:
            return []

        user_index = self.user_id_mapping[user_id]
        user_interactions = self.user_items_matrix[user_index]

        item_indices, scores = self.model.recommend(user_index, user_interactions, N=N)

        recommended_ids = [self.item_index_mapping[int(idx)] for idx in item_indices]
        return recommended_ids

recommender_service = ALSRecommender()
