"""
AIVibe Google Cloud Knowledge Module

Complete GCloud CLI patterns, Cloud Run, Firestore,
Cloud Functions, and GCP best practices.
"""


class GCloudKnowledge:
    """Comprehensive Google Cloud development knowledge."""

    CLI_VERSION = "500.0"
    PROJECT_ID = "${PROJECT_ID}"

    CLI_COMMANDS = {
        "configuration": {
            "init": "gcloud init",
            "auth_login": "gcloud auth login",
            "auth_adc": "gcloud auth application-default login",
            "set_project": "gcloud config set project PROJECT_ID",
            "list_configs": "gcloud config configurations list",
            "create_config": "gcloud config configurations create myconfig",
            "activate_config": "gcloud config configurations activate myconfig",
            "get_account": "gcloud auth list",
        },
        "iam": {
            "list_sa": "gcloud iam service-accounts list",
            "create_sa": """
gcloud iam service-accounts create my-service-account \\
    --display-name="My Service Account" """,
            "create_key": """
gcloud iam service-accounts keys create key.json \\
    --iam-account=my-sa@project.iam.gserviceaccount.com""",
            "add_binding": """
gcloud projects add-iam-policy-binding PROJECT_ID \\
    --member="serviceAccount:my-sa@project.iam.gserviceaccount.com" \\
    --role="roles/storage.objectViewer" """,
        },
        "cloud_run": {
            "deploy": """
gcloud run deploy my-service \\
    --image=gcr.io/PROJECT_ID/my-image:latest \\
    --platform=managed \\
    --region=us-central1 \\
    --allow-unauthenticated""",
            "list_services": "gcloud run services list",
            "describe": "gcloud run services describe my-service --region=us-central1",
            "delete": "gcloud run services delete my-service --region=us-central1",
            "logs": "gcloud run services logs read my-service --region=us-central1",
            "update_env": """
gcloud run services update my-service \\
    --set-env-vars="KEY=value" \\
    --region=us-central1""",
        },
        "cloud_functions": {
            "deploy_http": """
gcloud functions deploy my-function \\
    --runtime=python312 \\
    --trigger-http \\
    --allow-unauthenticated \\
    --entry-point=main \\
    --region=us-central1""",
            "deploy_pubsub": """
gcloud functions deploy my-function \\
    --runtime=python312 \\
    --trigger-topic=my-topic \\
    --entry-point=main \\
    --region=us-central1""",
            "list": "gcloud functions list",
            "logs": "gcloud functions logs read my-function --region=us-central1",
            "call": "gcloud functions call my-function --data='{\"key\":\"value\"}'",
        },
        "cloud_storage": {
            "list_buckets": "gsutil ls",
            "create_bucket": "gsutil mb -l us-central1 gs://my-bucket",
            "list_objects": "gsutil ls gs://my-bucket/prefix/",
            "copy": "gsutil cp local-file gs://my-bucket/key",
            "sync": "gsutil -m rsync -r ./local-dir gs://my-bucket/prefix",
            "delete": "gsutil rm gs://my-bucket/key",
            "set_acl": "gsutil acl ch -u AllUsers:R gs://my-bucket/public-file",
        },
        "firestore": {
            "export": """
gcloud firestore export gs://my-bucket/firestore-backup \\
    --collection-ids=users,projects""",
            "import": """
gcloud firestore import gs://my-bucket/firestore-backup""",
        },
        "secrets": {
            "list": "gcloud secrets list",
            "create": "gcloud secrets create my-secret --replication-policy=automatic",
            "add_version": "echo -n 'secret-value' | gcloud secrets versions add my-secret --data-file=-",
            "access": "gcloud secrets versions access latest --secret=my-secret",
        },
    }

    CLOUD_RUN = {
        "dockerfile": """
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "main:app"]""",
        "cloud_build": """
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA', '.']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA']

  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'my-service'
      - '--image=gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA'
      - '--region=us-central1'
      - '--platform=managed'

images:
  - 'gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA'""",
        "service_yaml": """
# service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-service
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "0"
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/cpu-throttling: "false"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      containers:
        - image: gcr.io/PROJECT_ID/my-service:latest
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: "1"
              memory: "512Mi"
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: database-url
                  key: latest""",
    }

    CLOUD_FUNCTIONS = {
        "http_function": """
import functions_framework
from flask import jsonify, Request

@functions_framework.http
def main(request: Request):
    try:
        data = request.get_json(silent=True) or {}

        # Process request
        result = process_data(data)

        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Internal server error'}), 500""",
        "pubsub_function": """
import base64
import json
import functions_framework
from cloudevents.http import CloudEvent

@functions_framework.cloud_event
def main(cloud_event: CloudEvent):
    data = base64.b64decode(cloud_event.data['message']['data']).decode()
    message = json.loads(data)

    print(f"Processing message: {message}")
    process_message(message)""",
        "firestore_trigger": """
import functions_framework
from cloudevents.http import CloudEvent

@functions_framework.cloud_event
def main(cloud_event: CloudEvent):
    event_type = cloud_event['type']
    document_path = cloud_event.data['value']['name']

    if 'google.cloud.firestore.document.v1.created' in event_type:
        handle_create(cloud_event.data['value']['fields'])
    elif 'google.cloud.firestore.document.v1.updated' in event_type:
        handle_update(
            cloud_event.data['oldValue']['fields'],
            cloud_event.data['value']['fields']
        )
    elif 'google.cloud.firestore.document.v1.deleted' in event_type:
        handle_delete(cloud_event.data['oldValue']['fields'])""",
    }

    FIRESTORE = {
        "operations": """
from google.cloud import firestore

db = firestore.Client()

# Create/Update document
def create_user(user_id: str, data: dict) -> None:
    db.collection('users').document(user_id).set(data)

# Get document
def get_user(user_id: str) -> dict | None:
    doc = db.collection('users').document(user_id).get()
    return doc.to_dict() if doc.exists else None

# Update fields
def update_user(user_id: str, updates: dict) -> None:
    db.collection('users').document(user_id).update(updates)

# Delete document
def delete_user(user_id: str) -> None:
    db.collection('users').document(user_id).delete()

# Query documents
def get_active_users() -> list[dict]:
    docs = db.collection('users') \\
        .where('status', '==', 'active') \\
        .order_by('created_at', direction=firestore.Query.DESCENDING) \\
        .limit(100) \\
        .stream()
    return [doc.to_dict() for doc in docs]

# Batch operations
def batch_update(user_ids: list[str], update: dict) -> None:
    batch = db.batch()
    for user_id in user_ids:
        ref = db.collection('users').document(user_id)
        batch.update(ref, update)
    batch.commit()

# Transaction
def transfer_credits(from_user: str, to_user: str, amount: int) -> None:
    @firestore.transactional
    def update_in_transaction(transaction):
        from_ref = db.collection('users').document(from_user)
        to_ref = db.collection('users').document(to_user)

        from_doc = from_ref.get(transaction=transaction)
        if from_doc.get('credits') < amount:
            raise ValueError("Insufficient credits")

        transaction.update(from_ref, {'credits': firestore.Increment(-amount)})
        transaction.update(to_ref, {'credits': firestore.Increment(amount)})

    update_in_transaction(db.transaction())""",
        "subcollections": """
# Create subcollection document
db.collection('users').document(user_id) \\
    .collection('projects').document(project_id).set(project_data)

# Query subcollection
projects = db.collection('users').document(user_id) \\
    .collection('projects').stream()

# Collection group query (across all users)
all_projects = db.collection_group('projects') \\
    .where('status', '==', 'active').stream()""",
    }

    PUBSUB = {
        "publisher": """
from google.cloud import pubsub_v1
import json

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('PROJECT_ID', 'my-topic')

def publish_message(data: dict) -> str:
    message_bytes = json.dumps(data).encode('utf-8')
    future = publisher.publish(topic_path, message_bytes)
    return future.result()  # Returns message ID

def publish_with_attributes(data: dict, **attributes) -> str:
    message_bytes = json.dumps(data).encode('utf-8')
    future = publisher.publish(topic_path, message_bytes, **attributes)
    return future.result()""",
        "subscriber": """
from google.cloud import pubsub_v1

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('PROJECT_ID', 'my-subscription')

def callback(message):
    try:
        data = json.loads(message.data.decode('utf-8'))
        process_message(data)
        message.ack()
    except Exception as e:
        print(f'Error processing message: {e}')
        message.nack()

streaming_pull = subscriber.subscribe(subscription_path, callback=callback)

# Keep listening
streaming_pull.result()""",
    }

    BEST_PRACTICES = {
        "security": [
            "Use Workload Identity for GKE",
            "Enable VPC Service Controls",
            "Use Secret Manager for credentials",
            "Enable Cloud Audit Logs",
            "Apply least-privilege IAM",
        ],
        "cost": [
            "Use committed use discounts",
            "Set up billing budgets",
            "Use Cloud Run min instances wisely",
            "Enable Firestore TTL for temporary data",
        ],
        "reliability": [
            "Use regional resources for HA",
            "Enable Cloud Run CPU always allocated for latency",
            "Implement retry with exponential backoff",
            "Use Cloud Tasks for reliable async",
        ],
    }

    def get_all(self) -> dict:
        """Get complete GCloud knowledge."""
        return {
            "cli_version": self.CLI_VERSION,
            "cli_commands": self.CLI_COMMANDS,
            "cloud_run": self.CLOUD_RUN,
            "cloud_functions": self.CLOUD_FUNCTIONS,
            "firestore": self.FIRESTORE,
            "pubsub": self.PUBSUB,
            "best_practices": self.BEST_PRACTICES,
        }

    def get_cli_commands(self) -> dict:
        """Get GCloud CLI command reference."""
        return self.CLI_COMMANDS

    def get_cloud_run_patterns(self) -> dict:
        """Get Cloud Run patterns."""
        return self.CLOUD_RUN

    def get_firestore_patterns(self) -> dict:
        """Get Firestore patterns."""
        return self.FIRESTORE
