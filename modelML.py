from sklearn.preprocessing import MinMaxScaler

one_hot_data = pd.get_dummies(complete_data)
print(one_hot_data)

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(one_hot_data)

scaled_df = pd.DataFrame(scaled_data)

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

model = KMeans(n_clusters=2)
model.fit(scaled_df)

# Getting the cluster labels for each data point
cluster_labels = model.labels_

# Getting the cluster centers
cluster_centers = pd.DataFrame(scaler.inverse_transform(model.cluster_centers_), columns=one_hot_data.columns)
print(cluster_centers)

# Calculating the silhouette score
sil_score = silhouette_score(scaled_df, cluster_labels)

print(f'Silhouette Score: {sil_score}')

# TO DO:
# use grid search to fine tune model weights
# visualize clusters and accuracy with matplotlib