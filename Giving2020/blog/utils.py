def prepare_posts(request, *posts):
    for post in posts:
        post.updated = False
        post.downvoted = False

        if request.user.is_authenticated:
            if any(p.user == request.user for p in post.upvote_set.all()):
                post.upvoted = True

            if any(p.user == request.user for p in post.downvote_set.all()):
                post.downvoted = True

    return posts
