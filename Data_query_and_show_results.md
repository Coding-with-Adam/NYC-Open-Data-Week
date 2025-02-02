

Both Malini and me are working on building natural language queries over this dataset. This is a rought design of possible interface.

First few steps can be developed independently, integration into overall app: minimal - to start, possible improvement - drive other tabs 

1. Create a tab in the main app, create chat windows, load data, describe subset we are working with
2. Integrate text to dataframe (trying few frameworks). Run in verbose mode, show df subsetting or sql code in the window, show results.
   Experiment with both business questions and data subsetting. Provide answers both as text and as dataframe ("table")
3. Show results graphically - both with unrestricted ui generation like Juan did for financial data and limiting to plots already used in the rest of the project (maps, other graphs)
4. Drive other tabs from the selected datasubset.
5. Allow user to use multiple frameworks (dataframe agent, sql agents, anthropic directly (Can we do it via APIs?), gemini2.0 - try reasoning
6. Add user feedback function and log positive/negative feedback.
7. Review with energy and water experts, get the list of useful queries
8. Load supporting docs, possibly extract data definitions (this could be in the earlier step)
