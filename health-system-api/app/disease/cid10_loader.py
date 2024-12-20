import json, uuid
from app.config.infra.database import db
from app.disease.model import Disease

def load_cid10_data():
    with open('app/disease/cid10.json', 'r', encoding='utf-8') as file:
        cid10_data = json.load(file)

    for item in cid10_data:
        namespace = uuid.NAMESPACE_DNS  # You can also use any other namespace
        fixed_uuid = str(uuid.uuid5(namespace, item['codigo']))  # Using 'codigo' or 'nome' for the string
        print(item['codigo'])
        disease = Disease(
            id=fixed_uuid,
            name=item['nome'],
            code=item['codigo']
        )
        
        db.session.add(disease)
    
    db.session.commit()

load_cid10_data()
