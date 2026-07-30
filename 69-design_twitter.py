# Design Twitter
# Implement a mini Twitter supporting:
#   postTweet(userId, tweetId)
#   getNewsFeed(userId)   -> the 10 most recent tweet ids from the user and everyone
#                            they follow, newest first
#   follow(followerId, followeeId)
#   unfollow(followerId, followeeId)
# Example: postTweet(1,5) ; getNewsFeed(1) -> [5]
#          follow(1,2) ; postTweet(2,6) ; getNewsFeed(1) -> [6,5]


# Case 1: Optimal: per-user tweet lists plus a k-way merge with a heap
from collections import defaultdict
import heapq

class Twitter:
    def __init__(self):
        self.time = 0                  # a global counter giving every tweet an order
        self.tweets = defaultdict(list)      # userId -> list of (time, tweetId)
        self.following = defaultdict(set)    # userId -> set of userIds they follow

    def postTweet(self, userId, tweetId):
        self.tweets[userId].append((self.time, tweetId))
        self.time += 1                 # monotonic, so higher time == more recent

    def getNewsFeed(self, userId):
        heap = []
        # a user always sees their own tweets, whether or not they follow themselves
        feed_sources = self.following[userId] | {userId}

        # seed the heap with the NEWEST tweet from each source, then merge k lists
        for uid in feed_sources:
            if self.tweets[uid]:
                index = len(self.tweets[uid]) - 1
                time, tweet_id = self.tweets[uid][index]
                # negate time to get a max-heap on recency
                heapq.heappush(heap, (-time, tweet_id, uid, index))

        result = []
        while heap and len(result) < 10:
            _, tweet_id, uid, index = heapq.heappop(heap)
            result.append(tweet_id)
            if index > 0:              # pull that source's next-newest tweet
                next_index = index - 1
                time, next_tweet = self.tweets[uid][next_index]
                heapq.heappush(heap, (-time, next_tweet, uid, next_index))

        return result

    def follow(self, followerId, followeeId):
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        self.following[followerId].discard(followeeId)   # discard: no error if absent
# postTweet / follow / unfollow: O(1)
# getNewsFeed: O(f + 10 log f)   f = number of accounts followed
# Space: O(total tweets + total follow edges)
# Only 10 results are needed, so a full sort of every tweet is wasteful - the heap
# merges the per-user lists lazily and stops after 10 pops.


if __name__ == "__main__":
    twitter = Twitter()
    twitter.postTweet(1, 5)
    print(twitter.getNewsFeed(1), twitter.getNewsFeed(1) == [5])

    twitter.follow(1, 2)
    twitter.postTweet(2, 6)
    print(twitter.getNewsFeed(1), twitter.getNewsFeed(1) == [6, 5])   # newest first
    print(twitter.getNewsFeed(2), twitter.getNewsFeed(2) == [6])      # 2 does not follow 1

    twitter.unfollow(1, 2)
    print(twitter.getNewsFeed(1), twitter.getNewsFeed(1) == [5])      # 6 is gone

    # the feed is capped at 10 and must stay in newest-first order
    t2 = Twitter()
    for i in range(1, 13):
        t2.postTweet(1, i)
    feed = t2.getNewsFeed(1)
    print(feed, feed == [12, 11, 10, 9, 8, 7, 6, 5, 4, 3])

    # unfollowing something never followed must not raise
    t3 = Twitter()
    t3.unfollow(1, 99)
    print(t3.getNewsFeed(1), t3.getNewsFeed(1) == [])

    # interleaved tweets from two users must merge by real time order
    t4 = Twitter()
    t4.follow(1, 2)
    t4.postTweet(1, 100)
    t4.postTweet(2, 200)
    t4.postTweet(1, 300)
    print(t4.getNewsFeed(1), t4.getNewsFeed(1) == [300, 200, 100])
