import json, uuid
from app.config.infra.database import db
from app.medication.model import Medication

def load_med_data():
    with open('app/medication/cmed.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        namespace = uuid.NAMESPACE_DNS  # You can also use any other namespace
        fixed_uuid = str(uuid.uuid5(namespace, item['REGISTRO']))  # Using 'codigo' or 'nome' for the string
        print(item)
        disease = Medication(
            id=fixed_uuid,
            name=item['PRODUTO'],
            ean=item['EAN'],
            active_ingredient=item['PRINCIPIO ATIVO'],
            lab=item['LABORATORIO'],
            lab_cnpj=item['CNPJ'],
            register=item['REGISTRO'],
            therapeutic_class=item['CLASSE TERAPEUTICA'],
            presentation=item['APRESENTACAO'],
        )
        
        db.session.add(disease)
    
    db.session.commit()

load_med_data()
