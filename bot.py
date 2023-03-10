"""
Penny is a no-nonsense budget tracker bot.

~~~~~~~~~~~~~~~~~~~

Penny brings the budget CLI experience to Discord using the Discord API.

:license: MIT, see LICENSE for more details.

# TODO:

Feb 15 07:19:40 PM  You should consider upgrading via the
'/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip' command
"""
# import csv
import os
import random
import subprocess
import uuid
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

from db import DBHelper

###############################################################################

# Help usage description.
DESCRIPTION = """
Hello! I am Penny, your no-nonsense budget tracker bot.

Trained for Discord, I am here to keep you in line with your finance and
respond to your commands and generate text based on your inputs.
Feel free to use the '?help' command to see the list of available commands and
how to use them. Remember, a penny saved is a penny earned!

Here are some of the things I can do:
"""

CURRENCY = "$"

PATH_CSV_EXPENSES = "penny_expenses.csv"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

###############################################################################

# EXPENSES = []
INCOME = []

db = DBHelper()
db.setup()
bot = commands.Bot(command_prefix="/",
                   description=DESCRIPTION,
                   intents=intents)

###############################################################################

# def csv_read_store_expenses(path):
#     """
#     Read expenses from the CSV file.
#
#     Store them in a list of dictionaries.
#     """
#     with open(path, "r") as csv_file:
#         # csv_reader = csv.reader(csv_file, delimiter=" ", quotechar="|")
#         csv_reader = csv.DictReader(csv_file)
#         for row in csv_reader:
#             EXPENSES.append(row)
#     pass

# def read_file(path):
#     """Open csv file in reader mode ("r")."""
#     with open(path, "r") as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=" ", quotechar="|")
#         for row in csv_reader:
#             print(", ".join(row))
#     return csv_file
#

# csv_file = read_file(PATH_CSV_EXPENSES)

# def csv_write_expenses(path):
#     """Write expenses to the CSV file, from the list of dictionaries."""
#     with open(path, "w", newline="") as csv_file:
#         fieldnames = [
#             "id",
#             "amount",
#             "category",
#             "description",
#             "timestamp",
#         ]
#         # csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#         # csv_writer.writeheader()
#         # for expense in EXPENSES:
#         #     csv_writer.writerow(expense)
#     pass

# def app_add_write_expense(amount, category, description):
#     expense = {
#         "id": str(uuid.uuid4()),
#         "amount": amount,
#         "category": category,
#         "description": description,
#         "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
#     }
#     EXPENSES.append(expense)
#     # csv_write_expenses(PATH_CSV_EXPENSES)
#     pass
#

# Read expenses from the CSV file and store them in the list of expenses.
# csv_read_store_expenses(PATH_CSV_EXPENSES)
# Test add_write_expense function.
# app_add_write_expense("10", "Food", "Lunch at Subway")

###############################################################################


def pretty_expense_row(row):
    date, category, amount, description = (
        row[5],
        row[3],
        row[2],
        row[4],
    )
    data = [
        date,
        category,
        str(amount),
        description,
    ]
    return " ".join(data)


###############################################################################


@bot.event
async def on_ready():
    """Log the terminal when the bot is ready and connected to Discord."""
    print(f"Logged in as {bot.user}.")


# if isinstance(error, commands.CommandOnCooldown):
#     await ctx.send(f"Command being invoked is on cooldown: {str(error)}.
#     # Use '!help' to see available commands.") else:
@bot.event
async def on_command_error(ctx, error):
    """Inform user when a command raise an error."""
    await ctx.send(f"An error occurred: {str(error)}")


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    """
    Log out the bot and disconnect it from the Discord API.

    This command can only be used by the owner of the bot.
    Once executed, the bot will be shut down and no longer respond to commands.

    Usage: ?shutdown

    Example:
        ?shutdown

    """
    await ctx.bot.logout()


###############################################################################

ping_limit_count = "6"


def ping_subprocess(target_host):
    """
    Construct a ping command with 6 packets.

    Runs it using subprocess.Popen, and capture the output in output and error
    variables. If there is an error, the function returns an error message
    with the error text.
    Otherwise, it returns the output in a readable format surrounded by triple
    backticks (```) to indicate code block formatting in Discord.
    """
    cmd = ["ping", "-c", ping_limit_count, target_host]  # Ping 6 times.
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        return "Error: " + error.decode("utf-8")
    else:
        return "```\n" + output.decode("utf-8") + "```"


@bot.command()
async def ping(ctx, target=None):
    """
    Ping the bot to test if it's responding.

    ?ping archlinux.org
    """
    await ctx.send("Pong!")
    # response = ping_subprocess(target)
    # await ctx.send(response)
    pass


###############################################################################


@bot.command(name="addexpense")
async def add_expense(ctx, amount: float, category: str, description: str):
    """Add a new expense to your budget."""
    expense = {
        "id": str(uuid.uuid4()),
        "amount": amount,
        "category": category,
        "description": description,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # EXPENSES.append(expense)
    # csv_write_expenses(PATH_CSV_EXPENSES)
    db.add_expense(
        uuid=expense["id"],
        user_id=ctx.author.id,
        amount=expense["amount"],
        category=expense["category"],
        description=expense["description"],
    )
    await ctx.send(
        f"New expense added: {CURRENCY}{amount} in {category} category")


# @bot.command(name="viewexpense")
# async def view_expense(ctx):
#     """View a rnadom expense in your budget."""
#     rand = random.choice(range(0, len(EXPENSES)))
#     counter = 0
# for expense in EXPENSES:
#     if counter == rand:
#         await ctx.send(
#             f"Random expense: {expense['description']} - {expense['amount']}{CURRENCY}"
#         )
#     counter += 1


@bot.command(name="deleteexpense")
async def delete_expense(ctx, keyword=None):
    expenses = db.get_expenses(user_id=ctx.author.id)
    if keyword is None:
        counter = 0
        pretty_expenses = []
        for row in expenses:
            expense = f"({counter}). {str(pretty_expense_row(row=row))}"
            pretty_expenses.append(expense)
            counter += 1

        await ctx.send(f"Select the (row) to delete")
        message = "\n".join(pretty_expenses)
        await ctx.send(f"""```{message}```""")
        row_index = await bot.wait_for(
            "message",
            check=lambda message: message.author == ctx.author,
        )

        index = int(row_index.content)  # Add error handling if not number...
        row_to_delete = pretty_expense_row(row=expenses[index])

        await ctx.send(f"""Deleting: {row_to_delete}\nAre you sure? (y/n)""")
        is_ok_delete = await bot.wait_for(
            "message",
            check=lambda message: message.author == ctx.author,
        )

        if (is_ok_delete.content).lower() in ["Y", "y"]:
            if db.delete_expense(user_id=ctx.author.id,
                                 uuid=(expenses[index])[0]):
                await ctx.send(f"Deleted {row_to_delete}")
        else:
            await ctx.send(f"Error: Something went wrong")
    pass


@bot.command(name="searchexpenses")
async def search_expenses(ctx, keyword: str):
    matches = db.search_expense(user_id=ctx.author.id, keyword=keyword)
    if matches is None:
        await ctx.send("No expenses matching '{keyword}' found")
    else:
        matches_pretty = []
        for row in matches:
            expense = pretty_expense_row(row)
            matches_pretty.append(expense)

        body = "\n".join(matches_pretty)
        count = len(matches)
        if count == 1:
            await ctx.send(
                f"```@expenses: {count} result found for {keyword}\n{body}```")
        else:
            await ctx.send(
                f"```@expenses: {count} results found for {keyword}\n{body}```"
            )
    pass


@bot.command(name="viewexpenses")
async def view_expenses(ctx):
    """View all expenses in your budget."""
    expenses = db.get_expenses(user_id=ctx.author.id)

    pretty = []
    total = 0
    for e in expenses:
        date, category, amount, description = e[5], e[3], e[2], e[4]
        pretty.append(" ".join([date, category, str(amount), description]))
        total += float(amount)

    counter = len(pretty)
    pretty_expenses = "\n".join(pretty)
    await ctx.send(f"Total expenses({str(counter)}): {str(total)}{CURRENCY}")
    await ctx.send(f"""```@expenses\n{pretty_expenses}```""")

    # fmt_time = expense["timestamp"].strftime("%v %d %y %I:%M:%S %p")
    # if len(EXPENSES) == 0:
    #     await ctx.send("No expenses recorded")
    # else:
    #     total = 0
    #     for expense in EXPENSES:
    #         total += float(expense["amount"])
    #         await ctx.send(
    #             f"[{expense['timestamp']}] {expense['category']}: {CURRENCY}{expense['amount']} - {expense['description']}"
    #         )
    #     await ctx.send(f"Total expenses: {str(total)}{CURRENCY}")
    #     # await ctx.send(f"Your Expenses \n{str(expenses)}")


###############################################################################

# Get the Discord bot token from the environment variable
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    print("The Discord token is not set")
    exit()

print("Starting bot server")

# Run the bot.
bot.run(TOKEN)

###############################################################################

# @bot.command(name="search-expenses")
# async def search_expenses(ctx, term: str):
#     """
#     Search expenses based on a term.
#
#     Takes a term argument which is used to filter the expenses list based on
#     any field that matches the search term (using the in operator and
#     case-insensitive string comparison). Send a message to the user with any
#     matching expenses, total amount, and a timestamp for each expense.
#     """
#     matches = [e for e in EXPENSES if term.lower() in str(e).lower()]
#     if len(matches) == 0:
#         await ctx.send(f"No expenses matching '{term}' found")
#     else:
#         total_matches_amount = sum(float(e["amount"]) for e in matches)
#         for expense in matches:
#             response = f"[{expense['timestamp']}] {expense['category']}:\
#                 {CURRENCY}{expense['amount']} {expense['description']}"
#
#             await ctx.send(response)
#         await ctx.send(
#             f"Total expenses({len(matches)}): {CURRENCY}{total_matches_amount}"
#         )
#
