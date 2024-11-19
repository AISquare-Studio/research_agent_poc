#!/usr/bin/env python
import sys
import redis
from research_agent_poc.crew import ResearchAgentPocCrew

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

SUB_CHANNEL = 'test'
PUB_CHANNEL = 'test2'


def run():
    """
    Run the crew.
    """
    # Connect to the database
    redis_client = redis.Redis(
        host='redis-16263.c44.us-east-1-2.ec2.redns.redis-cloud.com',
        port=16263,
        password='ES4hSBs0nGGPsreFdfssoooUQZbN9nKH',
        decode_responses=True
    )

    # Create a PubSub object that subscribes to channels and listens for new messages.
    pub_sub = redis_client.pubsub()

    # Subscribe to 'test' channel
    pub_sub.subscribe(SUB_CHANNEL)

    # Listen for messages
    for message in pub_sub.listen():
        message = pub_sub.get_message()
        if message['type'] == 'message':
            response = ResearchAgentPocCrew().crew().kickoff(
                inputs={'location': message['data']}
            )
            redis_client.publish(PUB_CHANNEL, response)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'location': 'Salt Lake City, Utah, USA'
    }
    try:
        ResearchAgentPocCrew().crew().train(n_iterations=int(
            sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ResearchAgentPocCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'location': 'Salt Lake City, Utah, USA'
    }
    try:
        ResearchAgentPocCrew().crew().test(n_iterations=int(
            sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
