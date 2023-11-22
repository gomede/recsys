import scipy.sparse as sp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Import the ratings dataset
ratings = pd.read_csv('Raw Dataset/Ratings.csv', sep=';')

num_observation = 10

# Select a subset of users and books for visualization
subset_users = ratings['User-ID'].unique()[:num_observation]  # First num_observation users
subset_books = ratings['ISBN'].unique()[:num_observation]  # First num_observation books

# Filter the ratings for the subset
subset_ratings = ratings[ratings['User-ID'].isin(subset_users) & ratings['ISBN'].isin(subset_books)]

# Mapping user IDs and ISBNs to matrix indices for the subset
user_indices = {user_id: index for index, user_id in enumerate(subset_users)}
book_indices = {book_isbn: index for index, book_isbn in enumerate(subset_books)}

# Creating the sparse matrix for the subset
rows = subset_ratings['User-ID'].map(user_indices)
cols = subset_ratings['ISBN'].map(book_indices)
data = subset_ratings['Rating']

sparse_matrix = sp.coo_matrix((data, (rows, cols)), shape=(num_observation, num_observation))

# Converting the sparse matrix to a dense format for heatmap visualization
dense_matrix = sparse_matrix.toarray()

# Visualizing the matrix using Seaborn heatmap
plt.figure(figsize=(10, 10))
sns.heatmap(dense_matrix, annot=False, cmap='Blues')
plt.title('Heatmap of User-Book Ratings (Subset)')
plt.xlabel('Books')
plt.ylabel('Users')
plt.show()


# Count of ratings per user
user_rating_counts = ratings['User-ID'].value_counts()

# Count of ratings per book
book_rating_counts = ratings['ISBN'].value_counts()

# Sorting the counts
user_rating_counts_sorted = user_rating_counts.sort_values(ascending=False)
book_rating_counts_sorted = book_rating_counts.sort_values(ascending=False)

# Plotting the long tail for users
plt.figure(figsize=(15, 6))
plt.subplot(1, 2, 1)
plt.plot(user_rating_counts_sorted.values)
plt.title('Long Tail Plot of User Ratings')
plt.xlabel('Users')
plt.ylabel('Number of Ratings')

# Plotting the long tail for books
plt.subplot(1, 2, 2)
plt.plot(book_rating_counts_sorted.values)
plt.title('Long Tail Plot of Book Ratings')
plt.xlabel('Books')
plt.ylabel('Number of Ratings')

plt.tight_layout()
plt.show()

# Extracting unique counts
unique_users = ratings['User-ID'].nunique()
unique_books = ratings['ISBN'].nunique()

# Total possible ratings
total_possible_ratings = unique_users * unique_books

# Actual ratings
actual_ratings = len(ratings)

# Calculating sparsity
sparsity = 1 - (actual_ratings / total_possible_ratings)
sparsity_percentage = sparsity * 100

print(f"Sparsity Percentage: {sparsity_percentage:.5f}%")