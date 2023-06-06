from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior, )
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import datetime
from kivymd.uix.datatables import MDDataTable
import json
import csv
class Gridlayout(GridLayout):
    pass
from kivy.core.window import Window

from kivy.config import Config
Config.set('kivy', 'window_icon', 'Images/icon1.png')


activities=[]

class RectangularElevationButton(RectangularRippleBehavior, CommonElevationBehavior, ButtonBehavior,
                                 BackgroundColorBehavior):
    pass


class CardExample(MDCard):
    pass


class CardScreen(Screen):
    pass


class ScreenManager1(ScreenManager):
    pass


class HomeScreen(Screen, BoxLayout):
    pass

class DataHolder:
    activities = []

def save_activities_to_json(activities, filename):
    with open(filename, 'w') as file:
        print('file created')
        json.dump(activities, file)


def load_activities_from_json(filename):
    with open(filename, 'r') as file:
        activities = json.load(file)
        return activities


class SecondScreen(Screen):
    def display_button_pressed(self):
        display_screen_instance = self.manager.get_screen('display_screen')
        display_screen_instance.show_timetable()
        self.manager.current = 'display_screen'
        self.manager.transition.direction = 'left'

    def update_button_pressed(self):
        update_screen_instance = self.manager.get_screen('update_screen')
        update_screen_instance.update_timetable()
        self.manager.current = 'update_screen'
        self.manager.transition.direction = 'left'

    def delete_button_pressed(self):
        delete_screen_instance = self.manager.get_screen('delete_screen')
        delete_screen_instance.delete_timetable()
        self.manager.current = 'delete_screen'
        self.manager.transition.direction = 'left'

    def csv_button_pressed(self):
        self.manager.current = 'csv_screen'
        self.manager.transition.direction = 'left'

    def reminder_button_pressed(self):
        reminder_screen_instance = self.manager.get_screen('reminder_screen')
        reminder_screen_instance.reminder()
        self.manager.current = 'reminder_screen'
        self.manager.transition.direction = 'left'


class LayoutScreen(Screen, ScrollView):
    pass


class QuestionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        inner_grid = GridLayout()
        inner_grid.cols = 2
        global start_time
        global end_time
        global time_period
        inner_grid.add_widget(
            Label(text='Enter the time you wakeup in\n HH:MM AM/PM format: ', color=[0, 0, 0, 1],
                  font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=None, height=70))
        start_time = TextInput(multiline=False, size_hint_y=None, height=70)
        inner_grid.add_widget(start_time)
        inner_grid.add_widget(Label(size_hint_y=.05))
        inner_grid.add_widget(Label(size_hint_y=.05))
        inner_grid.add_widget(
            Label(text='Enter the time you sleep in\n HH:MM AM/PM format:', color=[0,0,0, 1],
                  font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=None, height=70))
        end_time = TextInput(multiline=False, size_hint_y=None, height=70)
        inner_grid.add_widget(end_time)
        inner_grid.add_widget(Label(size_hint_y=.05))
        inner_grid.add_widget(Label(size_hint_y=.05))
        inner_grid.add_widget(
            Label(text='Enter the time period in\n hours:minutes format:', color=[0,0,0, 1],
                  font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=None, height=70))
        time_period = TextInput(multiline=False, size_hint_y=None, height=70)
        inner_grid.add_widget(time_period)
        outer_box = BoxLayout(orientation='vertical', padding=40, spacing=30)
        outer_box.add_widget(inner_grid)

        submit_button = Button(text='Submit', size_hint_y=.1, size_hint_x=.3, pos_hint={'center_x': .5},
                               font_name="Fonts/Somatic-Rounded.ttf", font_size=20,
                               background_color=[38/255, 70/255, 83/255, 1], background_normal='')
        submit_button.bind(on_press=self.submit_button_callback)
        outer_box.add_widget(submit_button)
        self.add_widget(outer_box)

    def validate_time_format(self, input_time, format_string):
        try:
            datetime.datetime.strptime(input_time, format_string)
            return True
        except ValueError:
            return False

    def submit_button_callback(self, instance):
        # validate time format for start_time and end_time
        if not self.validate_time_format(start_time.text, "%I:%M %p") or not self.validate_time_format(end_time.text,
                                                                                                       "%I:%M %p"):
            return

        # validate time format for time_period
        if not self.validate_time_format(time_period.text, "%H:%M"):
            return

        # pass start_time and end_time values as arguments to the second_question_screen instance
        self.manager.current = 'second_question_screen'
        self.manager.get_screen('second_question_screen').initialize(start_time.text, end_time.text)


class second_question_screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create a GridLayout with 2 rows and 2 columns
        self.inner_grid = GridLayout(cols=2, size_hint_y=None, spacing=10)
        self.inner_grid.bind(minimum_height=self.inner_grid.setter('height'))

        self.start_time = None
        self.end_time = None
        self.text_inputs = []
        self.repeat_button = None  # Declare the repeat_button attribute
        self.i = 0

    def initialize(self, start_time, end_time):
        # check if start_time and end_time have been entered
        if not start_time or not end_time:
            return

        # convert input to datetime objects
        self.start_time = datetime.datetime.strptime(start_time, "%I:%M %p")
        self.end_time = datetime.datetime.strptime(end_time, "%I:%M %p")

        # extract hours and minutes from time period input
        time_period_hours, time_period_minutes = map(int, time_period.text.split(':'))
        current_time_obj = self.start_time

        def repeat_loop(instance):
            nonlocal current_time_obj
            global activity
            self.inner_grid.clear_widgets()  # Clear all widgets before adding new ones
            while current_time_obj < self.end_time:
                current_time_str = current_time_obj.strftime("%I:%M %p")
                current_time_obj += datetime.timedelta(hours=time_period_hours, minutes=time_period_minutes)
                y = current_time_obj.strftime("%I:%M %p")
                self.inner_grid.add_widget(
                    Label(text=f"What activity do you perform \nbetween {current_time_str} and {y}? ",
                          color=[0, 0, 0, 1],
                          font_name="Fonts/Somatic-Rounded.ttf", font_size=20,
                          size_hint_y=None, height=50))

                self.activity = TextInput(multiline=False)
                self.text_inputs.append(self.activity)
                self.inner_grid.add_widget(self.activity)
                self.inner_grid.add_widget(
                    Label(text="Do you repeat this activity\n on other days? (Yes/No) ", color=[0, 0, 0, 1],
                          font_name="Fonts/Somatic-Rounded.ttf", font_size=20,
                          size_hint_y=None, height=50))
                repeat = TextInput(multiline=False)
                self.inner_grid.add_widget(repeat)

                def on_repeat_text_validate(repeat):


                    if repeat.text.lower() == "yes":
                        repeat.disabled = True
                        self.activity.disabled = True
                        self.inner_grid.add_widget(Label(
                            text=f"On which days do you repeat the\n activity '{self.activity.text}'?\n (comma-separated or type 'all'): ",
                            color=[0, 0, 0, 1],
                            font_name="Fonts/Somatic-Rounded.ttf", font_size=20,
                            size_hint_y=None, height=60))
                        days = TextInput(multiline=False)
                        self.inner_grid.add_widget(days)

                        def on_days_text_validate(days):
                            days.disabled = True
                            if days.text.lower() == 'all':
                                days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                            else:
                                days = days.text.lower().split(",")

                            global activities_for_multiple_days
                            activities_for_multiple_days = {day.strip(): self.activity.text for day in days}
                            print(activities_for_multiple_days)

                            activity_row = [f"{current_time_str}-{y}"]
                            def loop_repeat(activity_row):

                                day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                                while self.i < len(day):
                                    if day[self.i] in activities_for_multiple_days:
                                        activity_row.append(activities_for_multiple_days[day[self.i]])
                                        self.i += 1

                                    else:

                                        self.inner_grid.add_widget(Label(
                                            text=f"What do you do during the\n same time on {day[self.i].capitalize()}? ",
                                            color=[0, 0, 0, 1],
                                            font_name="Fonts/Somatic-Rounded.ttf", font_size=20,
                                            size_hint_y=None, height=50))
                                        activity_value = TextInput(multiline=False)
                                        self.text_inputs.append(activity_value)
                                        self.inner_grid.add_widget(activity_value)

                                        def on_activity_value(instance):
                                            activity_value.disabled = True
                                            activity_row.append(activity_value.text)
                                            self.i += 1

                                            loop_repeat(activity_row)

                                        activity_value.bind(on_text_validate=on_activity_value)

                                        break

                                if len(activity_row) == 8:

                                    DataHolder.activities.append(activity_row)
                                    print('hello')
                                    print(DataHolder.activities)
                                    self.i = 0
                                    # Check if all text inputs have been filled
                                    if all(text_input.text for text_input in self.text_inputs):
                                        self.repeat_button.disabled = False

                            loop_repeat(activity_row)

                            if all(text_input.text for text_input in self.text_inputs):
                                self.repeat_button.disabled = False  # Enable repeat button



                        days.bind(on_text_validate=on_days_text_validate)

                    elif repeat.text.lower() == "no":
                        repeat.disabled = True
                        self.activity.disabled = True
                        activity_row = [f"{current_time_str}-{y}"]
                        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                        for day in days:
                            self.inner_grid.add_widget(Label(
                                text=f"What do you do during \nthe same time on {day.capitalize()}? ",
                                color=[0, 0, 0, 1],
                                font_name="Fonts/Somatic-Rounded.ttf", font_size=20,
                                size_hint_y=None, height=50))
                            activity = TextInput(multiline=False)
                            self.text_inputs.append(activity)
                            self.inner_grid.add_widget(activity)

                            def on_n_text_validate(activity):
                                activity.disabled = True
                                activity_row.append(activity.text)
                                if len(activity_row) == 8:
                                    print(activity_row)
                                    DataHolder.activities.append(activity_row)
                                    print(DataHolder.activities)
                                    # Check if all text inputs have been filled
                                    if all(text_input.text for text_input in self.text_inputs):
                                        self.repeat_button.disabled = False

                            activity.bind(on_text_validate=on_n_text_validate)

                repeat.bind(on_text_validate=on_repeat_text_validate)
                break

            print(DataHolder.activities)
            if current_time_obj >= self.end_time:
                self.repeat_button.disabled = True
                outer_box.add_widget(go_back_button)
                outer_box.remove_widget(self.repeat_button)  # Remove the Repeat button

        repeat_loop(None)

        self.repeat_button = Button(text="Next", size_hint=(1, None), height=50,
                                    font_name="Fonts/Somatic-Rounded.ttf", font_size=20, disabled=True, background_color = [163/255, 196/255, 243/255], background_normal='', color=[0,0,0,1])
        self.repeat_button.bind(on_press=repeat_loop)

        scroll_view = ScrollView()
        scroll_view.add_widget(self.inner_grid)

        go_back_button = Button(text="Go Back", size_hint=(1, None), height=50,
                                font_name="Fonts/Somatic-Rounded.ttf", font_size=20, background_color = [163/255, 196/255, 243/255], background_normal='', color=[0,0,0,1])
        go_back_button.bind(on_press=self.go_back)

        outer_box = BoxLayout(orientation='vertical', padding=40, spacing=30)
        outer_box.add_widget(scroll_view)
        outer_box.add_widget(self.repeat_button)

        self.add_widget(outer_box)



    def go_back(self, instance):
        save_activities_to_json(DataHolder.activities, 'activities.json')
        self.manager.current = 'SecondScreen'
        self.manager.get_screen('SecondScreen')
        self.inner_grid.parent.remove_widget(self.inner_grid)



class ImageExample(Image):
    pass


class display_screen(Screen):
    def show_timetable(self):
        loaded_activities = load_activities_from_json('activities.json')
        if loaded_activities:
            DataHolder.activities = loaded_activities
        print(DataHolder.activities)
        self.clear_widgets()
        # create a BoxLayout for the screen
        box_layout = BoxLayout(orientation='vertical', padding=30)
        print(DataHolder.activities)

        # check if activities list is empty
        if len(DataHolder.activities) == 0:
            # add a label to the BoxLayout
            box_layout.add_widget(
                Label(text='No Timetable Is Created', color=[0, 0, 0, 1], font_name="Fonts/Somatic-Rounded.ttf",
                      font_size=35))
            go_back_button = Button(text='Go Back To Home Screen', font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=.1, size_hint_x=.25, pos_hint={'center_x':.5}, background_color=[231/255, 227/255, 147/255], background_normal='', color=[0,0,0,1])
            box_layout.add_widget(go_back_button)

            go_back_button.bind(on_press=self.go_back_to_home)

        if len(DataHolder.activities) != 0:
            table = MDDataTable(
                #background_color_header=[184/255, 213/255, 184/255],

                column_data=[
                    ('[color=4ecdc4]Time[/color]', dp(50)),
                    ('[color=4ecdc4]Monday[/color]', dp(30)),
                    ('[color=4ecdc4]Tuesday[/color]', dp(30)),
                    ('[color=4ecdc4]Wednesday[/color]', dp(35)),
                    ('[color=4ecdc4]Thursday[/color]', dp(35)),
                    ('[color=4ecdc4]Friday[/color]', dp(30)),
                    ('[color=4ecdc4]Saturday[/color]', dp(30)),
                    ('[color=4ecdc4]Sunday[/color]', dp(30))
                ],
                row_data=DataHolder.activities,
                padding=20
            )
            table.md_bg_color = [1, 0, 0, 1]
            box_layout.add_widget(table)
            box_layout.add_widget(Label(size_hint_y=.02))
            go_back_button = Button(text='Go Back To Home Page', size_hint_y=.1, size_hint_x=.2,
                                    pos_hint={'center_x': .5},font_name="Fonts/Somatic-Rounded.ttf", font_size=20, background_color=[241/255, 218/255, 196/255], background_normal='', color=[0,0,0,1])
            box_layout.add_widget(go_back_button)

            go_back_button.bind(on_press=self.go_back_to_home)

        self.add_widget(box_layout)  # Add the BoxLayout to the screen

    def go_back_to_home(self, instance):
        second_screen = self.manager.get_screen('SecondScreen')
        self.manager.current = 'SecondScreen'


class update_screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create a GridLayout with 2 rows and 2 columns
        self.inner_grid = GridLayout(cols=2, size_hint_y=None, spacing=10, padding=40)
        self.inner_grid.bind(minimum_height=self.inner_grid.setter('height'))

    def update_timetable(self):
        def repeat_loop(instance):
            loaded_activities = load_activities_from_json('activities.json')
            if loaded_activities:
                DataHolder.activities = loaded_activities
            days = {"monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6, "sunday": 7}
            ans = 'yes'
            # take input from user
            self.inner_grid.clear_widgets()
            while ans == 'yes':
                print(DataHolder.activities)
                self.inner_grid.add_widget(Label(text="What do you want to update?\n1. Replace one activity everywhere in the timetable\n2. Update 1 specific activity on a certain day and time", color=[1, 1, 1, 1], font_name="Fonts/Somatic-Rounded.ttf",
                                                 font_size=20, size_hint_y=None, height=100, size_hint_x=2))
                update_type = TextInput(multiline=False)
                self.inner_grid.add_widget(update_type)

                def update_type_validation(update_type):
                    print(DataHolder.activities)
                    if update_type.text == "1":
                        update_type.background_color = [173/255, 216/255, 230/255, 1]
                        update_type.disabled = True
                        print(DataHolder.activities)
                        self.inner_grid.add_widget(
                            Label(text="Enter the name of the activity you want to replace: ",color=[1, 1, 1, 1],
                                  font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=None, height=50))
                        old_activity = TextInput(multiline=False)
                        self.inner_grid.add_widget(old_activity)

                        def on_old_activity_validate(old_activity):
                            old_activity.background_color = [173 / 255, 216 / 255, 230 / 255, 1]
                            old_activity.disabled = True
                            self.inner_grid.add_widget(
                                Label(text="Enter the new name of the activity: ", color=[1, 1, 1, 1],
                                      font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=None, height=50))
                            new_activity = TextInput(multiline=False)
                            self.inner_grid.add_widget(new_activity)

                            def new_activity_validate(instance):
                                new_activity.background_color = [173 / 255, 216 / 255, 230 / 255, 1]
                                new_activity.disabled = True

                                self.inner_grid.add_widget(
                                    Label(text="The Activity Has been Updated", color=[1, 1, 1, 1],
                                          font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=None,
                                          height=50))

                                old_activity_text = old_activity.text
                                new_activity_text = new_activity.text
                                for activity_row in DataHolder.activities:
                                    for i in range(1, len(activity_row)):
                                        if activity_row[i] == old_activity_text:
                                            activity_row[i] = new_activity_text
                                print(DataHolder.activities)

                            new_activity.bind(on_text_validate=new_activity_validate)

                        old_activity.bind(on_text_validate=on_old_activity_validate)

                    elif update_type.text == "2":
                        update_type.background_color = [173 / 255, 216 / 255, 230 / 255, 1]
                        update_type.disabled = True
                        self.inner_grid.add_widget(
                            Label(text="Enter the day for which you want to update the activity: ", color=[1, 1, 1, 1],
                                  font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=None, height=50))
                        day = TextInput(multiline=False)

                        self.inner_grid.add_widget(day)

                        def on_day_text_validate(day):
                            day.background_color = [173 / 255, 216 / 255, 230 / 255, 1]
                            day.disabled = True
                            day = day.text.lower()
                            if day not in days:
                                self.inner_grid.add_widget(
                                    Label(text="Invalid day entered. Please try again.", color=[1, 1, 1, 1],
                                          font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=None,
                                          height=50))
                                return
                            day_index = days[day]
                            self.inner_grid.add_widget(
                                Label(
                                    text="Enter the time range for which you want to update the activity (in HH:MM AM/PM format): "
                                    , color=[1, 1, 1, 1],
                                    font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=None, height=50))
                            time_range_input = TextInput(multiline=False)
                            self.inner_grid.add_widget(time_range_input)

                            def on_timerange_text_validate(time_range_input):
                                time_range_input.background_color = [173 / 255, 216 / 255, 230 / 255, 1]
                                time_range_input.disabled = True
                                time_range_input = time_range_input.text.strip()  # remove leading/trailing whitespace
                                try:
                                    start_time, end_time = time_range_input.split(
                                        "-")  # split input into start and end time
                                    start_time = datetime.datetime.strptime(start_time.strip(), '%I:%M %p').strftime(
                                        '%I:%M %p')  # parse start time
                                    end_time = datetime.datetime.strptime(end_time.strip(), '%I:%M %p').strftime(
                                        '%I:%M %p')  # parse end time
                                except ValueError:
                                    self.inner_grid.add_widget(
                                        Label(
                                            text="Invalid time range entered. Please try again.", color=[1, 1, 1, 1],
                                            font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=None,
                                            height=50))
                                    return
                                activity_index = None
                                for i in range(len(DataHolder.activities)):
                                    if DataHolder.activities[i][0] == f"{start_time}-{end_time}":
                                        activity_index = i
                                        break
                                if activity_index is None:
                                    self.inner_grid.add_widget(
                                        Label(
                                            text="Invalid time range entered. Please try again.", color=[1, 1, 1, 1],
                                            font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=None,
                                            height=50))
                                else:
                                    self.inner_grid.add_widget(
                                        Label(text="Enter the new name of the activity: ", color=[1, 1, 1, 1],
                                              font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=None,
                                              height=50))
                                    newactivity = TextInput(multiline=False)
                                    self.inner_grid.add_widget(newactivity)

                                    def on_newactivity_text_validate(newactivity):
                                        newactivity.background_color = [173 / 255, 216 / 255, 230 / 255, 1]
                                        newactivity.disabled = True
                                        DataHolder.activities[activity_index][day_index] = newactivity.text


                                    newactivity.bind(on_text_validate=on_newactivity_text_validate)

                            print(DataHolder.activities)

                            time_range_input.bind(on_text_validate=on_timerange_text_validate)

                        day.bind(on_text_validate=on_day_text_validate)

                update_type.bind(on_text_validate=update_type_validation)

                break

        repeat_loop(None)
        repeat_button = Button(text="Update More Activities", size_hint=(1, None), height=50, font_name="Fonts/Somatic-Rounded.ttf",
                               font_size=20, color=[0, 0, 0, 1], background_color=[215 / 255, 249 / 255, 255 / 255],
                               background_normal='')
        repeat_button.bind(on_press=repeat_loop)

        scroll_view = ScrollView()
        scroll_view.add_widget(self.inner_grid)

        go_back_button = Button(text="Go Back", size_hint=(1, None), height=50,
                                font_name="Fonts/Somatic-Rounded.ttf", font_size=20, color=[0, 0, 0, 1],
                                background_color=[255 / 255, 237 / 255, 225 / 255], background_normal='')
        go_back_button.bind(on_press=self.go_back)

        outer_box = BoxLayout(orientation='vertical', padding=40, spacing=30)
        outer_box.add_widget(scroll_view)
        outer_box.add_widget(repeat_button)
        outer_box.add_widget(go_back_button)

        self.add_widget(outer_box)



    def go_back(self, instance):
        save_activities_to_json(DataHolder.activities, 'activities.json')
        self.manager.current = 'SecondScreen'
        self.manager.get_screen('SecondScreen')
        self.inner_grid.parent.remove_widget(self.inner_grid)

class delete_screen(Screen):
    def delete_timetable(self):
        self.clear_widgets()
        loaded_activities = load_activities_from_json('activities.json')
        if loaded_activities:
            DataHolder.activities = loaded_activities

        inner_grid = GridLayout(cols=2, padding=150)
        inner_grid.add_widget(Label())
        inner_grid.add_widget(Label())
        inner_grid.add_widget(Label(text='Are you sure you want to delete \nyour current timetable? (yes/no)',
                                    color=[0, 0, 0, 1], font_name="Fonts/Somatic-Rounded.ttf", font_size=25,
                                    size_hint_y=None, height=60))
        confirm = TextInput(multiline=False, size_hint_y=None, height=60)
        inner_grid.add_widget(confirm)
        inner_grid.add_widget(Label())
        inner_grid.add_widget(Label())

        def on_confirm_text_validate(confirm):
            if confirm.text.lower() == 'yes':
                DataHolder.activities.clear()
                self.clear_widgets()  # Clear all existing widgets from the screen

                inner_grid_result = GridLayout(cols=1, padding=60)
                inner_grid_result.add_widget(Label(text='The Timetable Has Been Deleted',
                                                   color=[0, 0, 0, 1], font_name="Fonts/Somatic-Rounded.ttf",
                                                   font_size=30))
                go_back_button = Button(text="Go Back To Home Screen", size_hint=(.5, None), height=50,
                                                     font_name="Fonts/Somatic-Rounded.ttf", font_size=25,
                                                     background_color=[42/255, 157/255, 143/255],
                                                     background_normal='')
                go_back_button.bind(on_press=self.go_back_to_home)
                inner_grid_result.add_widget(go_back_button)

                self.add_widget(inner_grid_result)  # Add the new layout to the screen
            elif confirm.text.lower() == 'no':
                second_screen = self.manager.get_screen('SecondScreen')
                self.manager.current = 'SecondScreen'

        confirm.bind(on_text_validate=on_confirm_text_validate)
        self.add_widget(inner_grid)

    def go_back_to_home(self, instance):
        save_activities_to_json(DataHolder.activities, 'activities.json')
        second_screen = self.manager.get_screen('SecondScreen')
        self.manager.current = 'SecondScreen'

class csv_screen(Screen):

    def go_next(self):
        csv_screen_instance = self.manager.get_screen('second_csv_screen')
        csv_screen_instance.export_csv()
        self.manager.current = 'second_csv_screen'
        self.manager.transition.direction = 'left'

class second_csv_screen(Screen):
    def export_csv(self):
        self.clear_widgets()
        loaded_activities = load_activities_from_json('activities.json')
        DataHolder.activities = loaded_activities
        main_layout = BoxLayout(orientation='vertical', spacing=20, padding=30)

        inner_grid = GridLayout(cols=2, spacing=20, padding=60)
        inner_grid.add_widget(Label())
        inner_grid.add_widget(Label())
        inner_grid.add_widget(
            Label(text='Enter the absolute path where u want to store the \ncsv file(Eg:- /Desktop/project/data/timetable.csv):', color=[0, 0, 0, 1],
                  font_name="Fonts/Somatic-Rounded.ttf", font_size=25, size_hint_y=None, height=60))
        path = TextInput(multiline=False,size_hint_y=None, height=60 )
        inner_grid.add_widget(path)

        button_layout = BoxLayout(orientation='horizontal', spacing=20, padding=10)
        go_back_button = Button(text="Go Back To Home Screen", size_hint=(1, None), height=50,
                                font_name="Fonts/Somatic-Rounded.ttf", font_size=20, background_color=[229/255, 249/255, 147/255], background_normal='', color=[0,0,0,1])
        go_back_button.bind(on_press=self.go_back_to_home)
        button_layout.add_widget(go_back_button)

        def on_path_text_validate(path):
            if path.text != '':
                file = open(path.text, 'w')
                writer = csv.writer(file)
                writer.writerow(['Time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
                writer.writerows(DataHolder.activities)
                file.close()
                self.clear_widgets()  # Clear all existing widgets from the screen

                inner_grid_result = GridLayout(cols=1, padding=20)
                inner_grid_result.add_widget(Label(text='The Timetable Has Been Exported to the csv file', color=[0, 0, 0, 1],
                                                   font_name="Fonts/Somatic-Rounded.ttf", font_size=25))
                go_back_button = Button(text="Go Back To Home Screen", size_hint=(1, None), height=50,
                                        font_name="Fonts/Somatic-Rounded.ttf", font_size=20, background_color=[229/255, 249/255, 147/255], background_normal='', color=[0,0,0,1])
                go_back_button.bind(on_press=self.go_back_to_home)

                inner_grid_result.add_widget(go_back_button)

                self.add_widget(inner_grid_result)
        path.bind(on_text_validate=on_path_text_validate)
        main_layout.add_widget(inner_grid)
        main_layout.add_widget(button_layout)

        self.add_widget(main_layout)
    def go_back_to_home(self, instance):
        save_activities_to_json(DataHolder.activities, 'activities.json')
        second_screen = self.manager.get_screen('SecondScreen')
        self.manager.current = 'SecondScreen'


class reminder_screen(Screen):
    def reminder(self):
        box_layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        box_layout.add_widget(Label(text='Feature Not yet Available', color=[0, 0, 0, 1], font_name="Fonts/Somatic-Rounded.ttf", font_size=35))
        back = Button(text='Go Back To Home Screen',font_name="Fonts/Somatic-Rounded.ttf", font_size=20, size_hint_y=.1, size_hint_x=.25, pos_hint={'center_x':.5}, background_color=[255/255, 127/255, 17/255], background_normal='', color=[0,0,0,1])
        back.bind(on_press=self.go_back_to_home)
        box_layout.add_widget(back)
        self.add_widget(box_layout)
    def go_back_to_home(self, instance):

        self.manager.current = 'SecondScreen'

class second_timetable_layout(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box_layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        box_layout.add_widget(
            Label(text='Feature Not yet Available', color=[0, 0, 0, 1], font_name="Fonts/Somatic-Rounded.ttf",
                  font_size=35))
        back = Button(text='Go Back To Home Screen', font_name="Fonts/Somatic-Rounded.ttf", font_size=20,
                      size_hint_y=.1, size_hint_x=.25, pos_hint={'center_x': .5},
                      background_color=[255 / 255, 127 / 255, 17 / 255], background_normal='', color=[0, 0, 0, 1])
        back.bind(on_press=self.go_back_to_home)
        box_layout.add_widget(back)
        self.add_widget(box_layout)
    def go_back_to_home(self, instance):

        self.manager.current = 'SecondScreen'


class HomeScreen1(BoxLayout):
    pass


class LabApp(MDApp):
    activities = []
    def build(self):

        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.theme_style = "Dark"
        self.icon = 'Images/icon1.png'

        Window.size = (1440, 800)

        # Calculate the position to center the window on the screen

        screen_width = Window.width
        screen_height = Window.height
        app_width, app_height = Window.size
        app_pos_x = (screen_width - app_width) // 2
        app_pos_y = (screen_height - app_height) // 2

        # Set the app window position
        Window.top = app_pos_y
        Window.left = app_pos_x

        # Add your app widgets to the root widget






LabApp().run()

