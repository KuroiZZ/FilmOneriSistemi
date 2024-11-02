import Normalize as normalize
from mlxtend.frequent_patterns import fpgrowth, association_rules

def CreateRules(minsupport, liftthreshold, writeFile):
    user_movie_matrix = normalize.CreateMatris(False)
    frequent_itemsets = fpgrowth(user_movie_matrix, min_support=minsupport, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=liftthreshold)
    if(writeFile):
        rules.to_csv("Rules/rules.csv", index=False)


































