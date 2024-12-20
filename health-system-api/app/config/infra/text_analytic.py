import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


class TextAnalytic:

    def __init__(self):
        ta_credential = AzureKeyCredential(os.environ["AZURE_HEALTH_KEY"])
        self.text_analytics_client = TextAnalyticsClient(
            endpoint=os.environ["AZURE_HEALTH_ENDPOINT"],
            credential=ta_credential,
            default_country_hint="BR",
            default_language="pt",
        )

    def analyze(self, text):
        documents = [text]

        poller = self.text_analytics_client.begin_analyze_healthcare_entities(documents)
        result = poller.result()

        docs = [doc for doc in result if not doc.is_error]

        return docs

    # Example function for extracting information from healthcare-related text
    def health_example(client):
        documents = [
            """
                 """
        ]

        poller = client.begin_analyze_healthcare_entities(documents)
        result = poller.result()

        docs = [doc for doc in result if not doc.is_error]

        for idx, doc in enumerate(docs):
            for entity in doc.entities:
                print("Entity: {}".format(entity.text))
                print("...Normalized Text: {}".format(entity.normalized_text))
                print("...Category: {}".format(entity.category))
                print("...Subcategory: {}".format(entity.subcategory))
                print("...Offset: {}".format(entity.offset))
                print("...Confidence score: {}".format(entity.confidence_score))
            for relation in doc.entity_relations:
                print(
                    "Relation of type: {} has the following roles".format(
                        relation.relation_type
                    )
                )
                for role in relation.roles:
                    print(
                        "...Role '{}' with entity '{}'".format(
                            role.name, role.entity.text
                        )
                    )
            print("------------------------------------------")
