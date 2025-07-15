from nltk.book import *



# concordance view shows us every occurrence of a given word, together with some
#context.
text1.concordance("monstrous")   

text2.concordance("book")

print("--------------------------")

text1.similar("monstrous")

text2.similar("book")


print("-----------------------------")

text3.common_contexts(["monstrous","very"])


#text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])

#text3.generate()

print(len(text3))


# sorted 
print("------------------sorted--------------------")
print(sorted(set(text3)))

print(f"length : {len(sorted(set(text3)))}")



print("-------------------------------------------")