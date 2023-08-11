import csv
import random
from datetime import datetime, timedelta

def generate_fake_data():
    # CSV1: Fake Collected Summary Data
    summary_rows = [['User', 'Week', 'Week Number', 'Collection & Compliance: Survey',
                     'Collection & Compliance: Data', 'Total Locations This Week',
                     'New Locations Visited', 'Average Significant Locations Per Day',
                     'Days Left Home', 'Average Daily Time Spent At Home']]

    # CSV2: Fake App Engagement Data
    engagement_rows = [['User', 'Week', 'Week Number', 'Page', 'Duration']]

    # CSV3: Fake Survey Response Data
    survey_rows = [['User', 'Week', 'Week Number', 'Survey', 'Question', 'Response']]

    user_count = 5
    week_count = 5 * 4  # Assuming 4 weeks per month for 5 months
    start_date = datetime(2023, 1, 1)

    for user in range(1, user_count + 1):
        for week in range(week_count):
            current_date = start_date + timedelta(weeks=week)
            week_number = week + 1
            survey_count = random.randint(1, 4)
            data_count = random.randint(1, 7)
            total_locations = random.randint(14, 21)
            new_locations_visited = random.randint(1, 7)
            avg_sig_locations_per_day = random.randint(1, 7)
            days_left_home = random.randint(1, 7)
            avg_daily_time_at_home = random.randint(2800, 57600)

            summary_rows.append([f'User{user}', current_date.strftime('%m/%d/%Y'), week_number,
                                 survey_count, data_count, total_locations,
                                 new_locations_visited, avg_sig_locations_per_day,
                                 days_left_home, avg_daily_time_at_home])

            # Generating data for Fake App Engagement Data
            pages = ['Feed', 'Learn', 'Access', 'Manage', 'Portal']
            for page in pages:
                if page in ['Feed', 'Learn']:
                    duration = random.randint(420, 1260)
                elif page in ['Access', 'Manage']:
                    duration = random.randint(4200, 8400)
                else:
                    duration = random.randint(1260, 4200)

                engagement_rows.append([f'User{user}', current_date.strftime('%m/%d/%Y'), week_number,
                                        page, duration])

            # Generating data for Fake Survey Response Data
            surveys = {
                'Depression': 9,
                'Satisfaction': 10,
                'Resilience': 8,
                'Critical Events': 10
            }

            for survey, num_questions in surveys.items():
                for question in range(1, num_questions + 1):
                    if survey == 'Critical Events':
                        response = random.randint(0, 1)
                    elif survey == 'Depression':
                        response = random.randint(0, 3)
                    else:
                        response = random.randint(0, 4)

                    survey_rows.append([f'User{user}', current_date.strftime('%m/%d/%Y'), week_number,
                                        survey, f'Question {question}', response])

    # Save CSV1
    with open('Fake_Collected_Summary_Data.csv', mode='w', newline='') as summary_file:
        summary_writer = csv.writer(summary_file)
        summary_writer.writerows(summary_rows)

    # Save CSV2
    with open('Fake_App_Engagement_Data.csv', mode='w', newline='') as engagement_file:
        engagement_writer = csv.writer(engagement_file)
        engagement_writer.writerows(engagement_rows)

    # Save CSV3
    with open('Fake_Survey_Response_Data.csv', mode='w', newline='') as survey_file:
        survey_writer = csv.writer(survey_file)
        survey_writer.writerows(survey_rows)

if __name__ == '__main__':
    generate_fake_data()
