phrases = [" in your pants", "... ladies", " in bed", " at night",
        " with your mother", "... that's what she said", " #420", " #swag",
        " #yolo", " LE MAYMAY", " so edgy", " #yoloswag"]

from random import choice
from utils import *

NAME="Immature phrase appender"
DESC="Makes anything people say immature."

def initModule(cod):
    cod.botcommands["IMMATURE"] = [commandIMMATURE]

def destroyModule(cod):
    del cod.botcommands["IMMATURE"]

def commandIMMATURE(cod, line, splitline, source, destination):
    cod.reply(source, destination, immature(" ".join(splitline[1:])))

def immature(tweet, no_url=True):
	"""
	A very childish function.

	takes any string input (assumes a sentence) and appends "in your
	pants" to it, preserving case if nessecary.

	only needs a special case if there is a URL in the tweet.
	"""
	conditions = [tweet.endswith("!"), tweet.endswith("."), tweet.endswith("?")]
	valid = reduce(lambda x,y: (x or y), conditions)
	#print valid

	if "http" in tweet.split()[-1]:
		return in_your_url(tweet, no_url)
		#jump to the special condition!
	elif ":" in tweet:
		return in_your_colon(tweet)

	if valid:
		split_tweet = tweet.split()

		derp = True

		if len(split_tweet) == 1:
			derp = False

		if derp and split_tweet[-2].isupper() and split_tweet[-1].isupper():
			return tweet[:-1] + choice(phrases).upper() + tweet[-1]
		else:
			return tweet[:-1] + choice(phrases) + tweet[-1]
	else:
		split_tweet = tweet.split()

		derp = True

		if len(split_tweet) == 1:
			derp = False

		if derp and split_tweet[-2].isupper() and split_tweet[-1].isupper():
			return tweet + choice(phrases).upper()
		else:
			return tweet + choice(phrases)

def in_your_url(tweet, no_url):
	"""
	Deals with URLs
	"""
	split_tweet = tweet.split()
	urlAtEnd = split_tweet[-1].startswith("http")

	if urlAtEnd:
		return immature(rejoin(split_tweet[:-1])) + " " + split_tweet[-1]
	else:
		return split_tweet[0] + " " + immature(split_tweet[1:])

def in_your_colon(tweet):
	return immature(str(tweet.split(":")[0])) + ":" + rejoin(tweet.split(":")[1:])

def rejoin(string_ara, delim=" "):
	try:
		r = str(reduce(lambda x,y: x + delim + y, string_ara))
	except:
		r = ""
	return r

def count(string, pattern):
	r = 0

	for n in string:
		if n == pattern:
			r = r + 1

	return r

def test():
    print immature("I am awesome.")
    print immature("SO COOL DRAGONITE!")
    print immature("check out my site! http://herp.derp")
    print immature("OPERATION SIMPLISTIC SALTY GREAT GRAPE RAPE APE")
    print immature("OPERATION EXPECT NO MERCY FROM OUR JUMBLED DISCOVERY")
    print immature("OPERATION TWISTING ADAPTABLE BREATH")

if __name__ == "__main__":
    test()
