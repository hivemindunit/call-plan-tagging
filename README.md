# Over Quota - Call Plan Tagging
API to match a set of call plan items or questions with a transcript section. The matching score is calculated by applying a BERT model (by default,
[all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2)).
- Input
    - transcript: String - _transcript section_
    - questions: [String] - _list of questions/call plan items_
- Output
  - index: Number - _index of a question/call plan item best matching with the transcript (with the highest score)_
  - score: Float - _matching score_
### Input Sample
```json
{
    "transcript": "Um so you mentioned data hygiene is not necessarily a challenge, but it sounds like it's those fields are required. So do you think that there would be, do you think you would be provided better visibility if reps were to enter in just better notes in general about their calls or are they already copy and pasting notes from Evernote and putting them into salesforce?",
    "questions": [
        "What’s the makeup of the sales team today, for example, the number of reps and how they are segmented?",
        "Could you describe the sales process, and provide details on the methodology and qualification framework used?",
        "How do you track adoption? Call recording, if so which solutions do you?",
        "What aspects of the sales process translate to fields in Salesforce?",
        "Is the process documented for reps? If so, how are they trained on it and access it?",
        "What software tools does the team use - tech validation, Zoom, Salesforce, current note-taking applications?",
        "How often are you joining calls with reps to help guide them through discovery calls or to close the deal?",
        "How do you provide support on those calls (slacking notes/prompts or taking over)?",
        "How would you rate data hygiene in Salesforce?",
        "Why do you think sales reps don’t like using Salesforce?",
        "How does that affect your pipeline visibility and forecasting capabilities?",
        "What have you tried to improve data hygiene in Salesforce?"
    ]
}
```
### Output Sample
```json
{
    "index": 11,
    "score": 0.5281470417976379
}
```

## Tech Stack
- [Serverless](https://www.serverless.com/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [SentenceTransformers](https://www.sbert.net/)
- [NLTK](https://www.nltk.org/)
## Deployment
### Set AWS Credentials 
Run `aws configure` and enter AWS credentials (Access Key ID and Secret Access Key).
### Create an ECR repository
This should be done only once, if the repository already exists, move on to the next step.
```shell
aws ecr create-repository --repository-name over-quota-call-plan-tagging
```
### Build Docker Image
```shell
docker build -t track-questions .
```
### Authenticate Docker CLI with AWS ECR
```shell
aws ecr get-login-password | docker login --username AWS --password-stdin 070835681152.dkr.ecr.us-east-1.amazonaws.com
```
### Tag the Image with the Repository URI
```shell
docker tag track-questions 070835681152.dkr.ecr.us-east-1.amazonaws.com/over-quota-call-plan-tagging
```
### Push the Image to ECR Repository
```shell
docker push 070835681152.dkr.ecr.us-east-1.amazonaws.com/over-quota-call-plan-tagging
```
### Deploy Lambda Function
```shell
serverless deploy
```
