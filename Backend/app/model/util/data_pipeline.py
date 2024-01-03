import os
import random

import pandas as pd

BASE_PATH = os.path.dirname(__file__)
READ_FILE_PATH = os.path.join(BASE_PATH, "..", "data", "customer_support_tickets.csv")
WRITE_FILE_PATH = os.path.join(BASE_PATH, "..", "data", "text_and_tickets.csv")
GREETING_PHRASES = (
    "Hello,\n",
    "Hello Support Team,\n\n",
)
GOODBYE_PHRASES = (
    "\n\nKind regards\n",
    "\nBest regards\n",
)


def read_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path, sep=",")


def fill_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = fill_text(df)
    df = fill_ticket(df)
    return df


def fill_text(df: pd.DataFrame) -> pd.DataFrame:
    df["text"] = df["Ticket Description"]
    df_sub = df[df["Ticket Channel"] == "Email"]
    df["text"][df["Ticket Channel"] == "Email"] = (
        pd.Series(random.choices(GREETING_PHRASES, k=df_sub.shape[0]))
        + df_sub["Ticket Description"]
        + pd.Series(random.choices(GOODBYE_PHRASES, k=df_sub.shape[0]))
        + df_sub["Customer Name"]
    )
    return df


def fill_ticket(df: pd.DataFrame) -> pd.DataFrame:
    df["ticket"] = pd.Series(
        [{
            "title": row["Ticket Subject"],
            "service": "",
            "category": "",
            "keywords": [],
            "customerPriority": "",
            "affectedPerson": row["Customer Name"],
            "description": row["Ticket Description"],
            "priority": row["Ticket Priority"],
            "requestType": row["Ticket Type"],
        } for _, row in df.iterrows()]
    )
    return df


def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df[["text", "ticket"]]


def write_data(file_path: str, df: pd.DataFrame):
    df.to_csv(file_path, index=False)


if __name__ == "__main__":
    df = read_data(READ_FILE_PATH)
    df = fill_columns(df)
    df = select_columns(df)
    write_data(WRITE_FILE_PATH, df)
