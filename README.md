# Anonymity and Free Speech: How Political Context Shapes Wikipedia Editors

### Group Members

Emma Kochenderfer  
Kal Fernande  
Dylan Boswell

### [Literature Review](https://github.com/kochenderferc/wikipedia-political-context/blob/main/literature-review.md)

## Abstract

Wikipedia aims to be a public encyclopedia, a place where people can share knowledge for the greater good. While its intentions- and those of most contributors– are noble, a few bad actors can move such a resource from being a public square– one where the sharing of information is done respectfully for the pursuit of the truth– to a tool to spread propaganda, misinformation and defamation for their own personal gain. Due to this problem, Wikipedia has incorporated an identification system, to track edits and comments on their wikipedia pages by a user’s IP address. This allows Wikipedia to at times restrict IP address editing access, if it is determined that a user is repeatedly vandalising the encyclopedia. While this system has successfully reduced the amount of spam and misinformation on the platform, it does bring up a series of other questions regarding user privacy, ease of contribution and user trust and has exposed a number of propagandised edits. We will research the link between Wiki and a user’s IP address for its impact on users who want to be critical of their government. Additionally, we’ll investigate the process of becoming a Wikipedia Administrator, how easy the role is to abuse, and what information administrators are privy to. Depending on that information, we’ll further research the meaning of this for a Wikipedia user who lives in a more repressive regime, and their trust in the wikipedia platform to preserve their anonymity. In asking these questions, we will determine the cost benefit analysis of anonymity versus spam protection to have the best outcomes for productive, constructive debate and discussion. We will then map the countries Wikipedia contributors come from and their respective laws protecting free speech and understand whether more draconian free speech laws are correlated with a decrease in wikipedia contributions and the impact of the IP address requirements.

## Research Questions

- How difficult is it to become a Wikipedia moderator?
- What different levels of power and information are moderators capable of having, and how difficult/easy are they able to abuse?
- What do these different roles and levels of information mean for Wikipedia users who live in more repressive regimes, and how is their anonymity protected?
- In terms of IP address restriction to avoid misuse of editing Wikipedia articles, how is it ensured that there is still space for free speech and constructive criticism and debate? How is this impacted by the regions that moderators are primarily from, and their internal biases?
- Where do the majority of Wikipedia contributors and moderators come from? What are the free speech laws like in those locations? How does the Wikipedia access of IP address for editors impact people in regions with less protected free speech?

## Methodology

We will examine Wikipedia policies for IP address tracking, administrator access and powers, and compare these with international/standards for free speech and data protection. We will look at previous cases of Wikipedia IP address blockings, such as the case where all users in Qatar were blocked from editing Wikipedia on accident in 2007. We will also look at countries where Wikipedia access is restricted or blocked by the government, such as in Myanmar and China. Using the Wikipedia API, we can track edits from different countries/regions of the world, anonymity vs. registered user edits, and administrator usage/number of admins for each region. We can use this information to check how the demographics for admins (country/free speech rights/political state) may impact their practices and usages of admin powers, and how countries with less protections on free speech has an impact on rates of edits/admins.

## Research Question Week 7

_INSTRUCTIONS DELETE THIS ONCE DONE! Explain a methodology involving the Wikipedia API of how to answer the question. (A small number of bullet points should be sufficient.)
Implement a Python script `week7.py` that helps answering the question.
Add instructions to the Readme that explain how to run the program. (A reader must be able to reproduce your results.)
Describe the results you obtain with the help of the program.
Explain how you are going to use the results of the program to answer your question._

#### Methodology

- Use the Wikipedia API to access the IP addresses of unregistered editors, then link those IP addresses to their respective countries.
- Run program for some period of time, then map frequency of edits per country.
- Compare frequency of edits for each country against benchmarks for national free speech.

#### Running the program

---

## ✅ How to Set Up and Run This Project

### 1. 🚀 Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/wikipedia-political-context.git
cd YOUR-REPOSITORY-NAME
```

> Replace `YOUR-USERNAME` with your GitHub username.

---

### 2. 🐍 Create and Activate a Virtual Environment

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. 📦 Install Project Dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

---

### 4. ▶️ Run the Program

To start the full pipeline (stream → save → visualize):

```bash
python week7.py
```

- This will run `data_streaming.py` for 10 seconds to collect edit data.
- It then automatically stops the script.
- Finally, it runs `data_visualizer.py` to display the data.

#### Results

With the help of the program, we can see a list of countries associated with edits made by unregistered users to English Wikipedia, then use that with our benchmark comparisons to see if there are patterns with edit frequency and how restrictive a government is with free speech.
