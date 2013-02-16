from django import template

register = template.Library()

@register.filter(is_safe=True)
def mission_time(mission):
    return " ".join([mission.day.strftime("%A"), mission.TIMES[mission.time]])


@register.tag('outcome')
def outcome(parser, token):
    return OutcomeNode()


class OutcomeNode(template.Node):
    """Return the outcome of a mission in an HTML class."""

    def render(self, context):
        mission = context['plot'].mission
        team = context['player'].team

        if mission.unfinished():
            return "unfinished"

        # If everyone wins a mission, we want each player to see their
        # team as winning.
        if mission.everyone_wins():
            victor = team
        else:
            victor = mission.victor

        return "_".join((victor, "won"))
