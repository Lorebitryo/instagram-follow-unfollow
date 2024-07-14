import instaloader
import argparse

def get_non_followers_and_non_following_back(username, password):
    L = instaloader.Instaloader()
    L.login(username, password)
    
    profile = instaloader.Profile.from_username(L.context, username)
    followers = set(profile.get_followers())
    followees = set(profile.get_followees())
    
    non_followers = followees - followers
    non_following_back = followers - followees
    
    return non_followers, non_following_back

def unfollow_non_followers(username, password):
    L = instaloader.Instaloader()
    L.login(username, password)
    
    non_followers, non_following_back = get_non_followers_and_non_following_back(username, password)
    
    if non_followers:
        print("You are about to unfollow the following users:")
        for non_follower in non_followers:
            print(non_follower.username)
        
        confirmation = input("Do you want to unfollow these users? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            for non_follower in non_followers:
                L.context.unfollow(non_follower.userid)
                print(f"Unfollowed {non_follower.username}")
        else:
            print("No users were unfollowed.")
    else:
        print("There are no users to unfollow.")
    
    if non_following_back:
        print("The following users follow you, but you do not follow them back:")
        for non_follower_back in non_following_back:
            print(non_follower_back.username)
        
        confirmation = input("Do you want to follow these users? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            for non_follower_back in non_following_back:
                L.context.follow(non_follower_back.userid)
                print(f"Followed {non_follower_back.username}")
        else:
            print("No users were followed.")
    else:
        print("There are no users who follow you that you don't follow back.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Unfollow non-followers and follow back followers on Instagram.')
    parser.add_argument('username', type=str, help='Your Instagram username')
    parser.add_argument('password', type=str, help='Your Instagram password')

    args = parser.parse_args()

    unfollow_non_followers(args.username, args.password)
