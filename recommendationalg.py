import random 

subjects = ["Algebra", "Calculus", "Geometry", "Physics", "Chemistry", "Engineering", "Biology", "Coding", "English", "History", "Geography", "French", "Spanish", "Chinese", "Latin"]
words = ["exciting", "life-changing", "mediocre", "novel", "worthless", "wonderful"]


def generate_posts():
    posts = []
    for _ in range(30):
        subject1 = random.choice(subjects)
        subject2 = random.choice(subjects) 
        while subject1 == subject2:
            subject2 = random.choice(subjects)
        subject3 = random.choice(subjects)
        while subject3 == subject1 or subject3 == subject2:
            subject3 = random.choice(subjects)
        
        title = f"A {random.choice(words)} Opportunity to explore the intersection of {subject1}, {subject2}, and {subject3}."

        posts.append({"title" : title, "weights" : {subject1 : 0.5, subject2 : 0.3, subject3 : 0.2}})

    return posts

#this will likely take in 2 dictionaries:
    #user contains a dict in a dict with all the user's weights towards certain subjects
    #post contains the weight information for each Opportunity
    #action is just like/dislike


#weights represent the likelihood of a user receiving Opportunities mainly in that field 
def update_weights(user, post, action):
    subjects_in_post = list(post["weights"].keys())

    if action == "like":
        sum = 0
        for subject in user["weights"]:
            sum += user["weights"][subject] * 0.1
            user["weights"][subject] *= 0.9 
        user["weights"][subjects_in_post[0]] += post["weights"][subjects_in_post[0]] * sum
        user["weights"][subjects_in_post[1]] += post["weights"][subjects_in_post[1]] * sum
        user["weights"][subjects_in_post[2]] += post["weights"][subjects_in_post[2]] * sum
    
    if action == "dislike":
        sum = 0
        for subject in user["weights"]:
            sum += user["weights"][subject] * 0.075
            user["weights"][subject] *= 1.075 
        user["weights"][subjects_in_post[0]] -= post["weights"][subjects_in_post[0]] * sum
        user["weights"][subjects_in_post[1]] -= post["weights"][subjects_in_post[1]] * sum
        user["weights"][subjects_in_post[2]] -= post["weights"][subjects_in_post[2]] * sum

def init_user():
    name = input("What is your name? ")

    for s in subjects:
        print(s, end=" ")

    weights = {}
    base_amt = 1 / (len(subjects) + 6)

    for s in subjects:
        weights[s] = base_amt

    print("\nOut of the above subjects, please enter your top 3 interests. ")

    inputs = [input() for i in range(3)]
    weights[inputs[0]] += 3 * base_amt
    weights[inputs[1]] += 2 * base_amt
    weights[inputs[2]] += 1 * base_amt

    user = {"username" : name, "weights" : weights}

    return user


user = init_user()
posts = generate_posts()

for post in posts[:10]:
    print("Here's an Opportunity!")
    print(post["title"])
    action = input("like or dislike: ")

    update_weights(user, post, action)

print(sorted(user["weights"].items(), key = lambda x:x[1], reverse=True))
