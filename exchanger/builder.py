from exchanger.models import Exchange


class Builder:
    # @staticmethod
    def exchange(self, base=None, date=None, goal=None, rate=None):
        exchange, created = Exchange.objects.get_or_create(
            base=base,
            date=date,
            goal=goal,
            rate=rate,
        )

        return created
