from sklearn.preprocessing import LabelEncoder

# Sample categorical labels
labels = ['red', 'blue', 'green', 'pink', 'red', 'Green', 'Orange']

# Initialize the LabelEncoder
label_encoder = LabelEncoder()

# Fit and transform the labels to numerical values
encoded_labels = label_encoder.fit_transform(labels)

print("Original Labels:", labels)
print("Encoded Labels:", encoded_labels)

# To decode back to original labels
decoded_labels = label_encoder.inverse_transform(encoded_labels)
print("Decoded Labels:", decoded_labels)