from .models import Activity

# formats activity list before send them to the template
def get_formatted_activities(user, activities):
    updated_activities = []

    for activity in activities:
        activity.likes = activity.likers.all()
        activity.logged_user_likes_activity = activity.likes.filter(user=user).exists()
        activity.location_name = dict(Activity.LOCATIONS)[activity.location]
        activity.game_mode_name = dict(Activity.GAME_MODES)[activity.game_mode]

        updated_activities.append(activity)

    return updated_activities