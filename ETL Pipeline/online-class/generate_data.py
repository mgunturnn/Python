import pandas as pd
from faker import Faker
import random

fake = Faker('id_ID')
data = []

# Membuat 1000 data palsu menggunakan Faker
for _ in range(1000):
    data.append({
        'client_id': fake.uuid4(),
        'name': fake.name(),
        'email': fake.email(),
        'course_name': random.choice(['Python Programming', 'Data Science', 'Web Development', 'Machine Learning']),
        'enrollment_date': fake.date_between(start_date='-1y', end_date='today'),
        'completion_status': random.choices(['Completed', 'In Progress', 'Not Started'], weights=[40, 50, 10])[0],
        'payment_status': random.choices(['Paid', 'Pending'], weights=[90, 10])[0]
    })

# Memgirim data ke dalam file CSV
df = pd.DataFrame(data)
df.to_csv('client_online_class.csv', index=False)
print("Selesai!, Cek Folder")