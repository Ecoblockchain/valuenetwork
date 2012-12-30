from decimal import *
from django.forms.widgets import MultiWidget, TextInput

class DurationWidget(MultiWidget):
    def __init__(self, attrs=None):
        _widgets = (
            TextInput(attrs={"class": "days",}),
            TextInput(attrs={"class": "hours",}),
            TextInput(attrs={"class": "minutes",}),
        )
        super(DurationWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        #import pdb; pdb.set_trace()
        if value:
            duration = int(value)
            days = duration / 1440
            hours = (duration - (days * 1440)) / 60
            minutes = duration - (days * 1440) - (hours * 60)
            return [days, hours, minutes]
        return [0, 0, 0]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        #import pdb; pdb.set_trace()
        dlist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        #todo: make more forgiving: change '' to 0
        try:
            duration = (int(dlist[0]) * 1440) + (int(dlist[1]) * 60) + int(dlist[2])
        except ValueError:
            return ''
        else:
            return duration


class DecimalDurationWidget(MultiWidget):
    def __init__(self, attrs=None):
        _widgets = (
            TextInput(attrs={"class": "days",}),
            TextInput(attrs={"class": "hours",}),
            TextInput(attrs={"class": "minutes",}),
        )
        super(DecimalDurationWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        #import pdb; pdb.set_trace()
        if value:
            duration = int(value)
            days = duration / 1440
            hours = duration - (days * 1440)
            mins = value - duration
            minutes = int((60 * mins).quantize(Decimal('1'), rounding=ROUND_UP))
            return [days, hours, minutes]
        return [0, 0, 0]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        #import pdb; pdb.set_trace()
        dlist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        #todo: make more forgiving: change '' to 0
        try:
            duration = Decimal((int(dlist[0]) * 1440) + (int(dlist[1]) * 60))
            duration += Decimal(dlist[2]) / 60
        except ValueError:
            return ''
        else:
            return duration
