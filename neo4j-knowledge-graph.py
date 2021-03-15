from neo4j import GraphDatabase
from dotenv import load_dotenv
from pathlib import Path
import os


dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD), encrypted=False)

def print_titles_subgraph(tx, userid):

    for record in tx.run("Match (n)-[r]-(m) WHERE n.userid = $userid "
                         "RETURN n,r,m LIMIT 100;", userid=userid):
        print(record["m.title"])

def main():
    with driver.session() as session:
        f = session.read_transaction(print_titles_subgraph, "612373254")
        print(f)
    driver.close()

if __name__ == "__main__":
    main()