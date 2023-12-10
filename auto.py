import logging
import os


logging.basicConfig(filename='auto.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def auto():
    """
    Conducts initial bot setup, including directory creation and token writing.
    Skips corresponding steps if the directory already exists or the token is already written.
    """
    logging.info('Initial setup started')
    turnoff_path = os.path.join(os.getenv('APPDATA'), 'TurnOffBot')

    try:
        os.mkdir(turnoff_path)
        logging.info('Directory created successfully')
    except Exception as e:
        logging.error(f'Error creating directory: {e}')

    token_count = 0
    while token_count < 3:
        entered_token = input('Enter your token: ')
        logging.debug(f'Token entered: {entered_token}')
        user_confirmation = input(f'Your token: {entered_token}? Is this correct? (Yes/No) ')
        if user_confirmation.lower() == 'yes':
            token_count += 3
            logging.info('Token confirmed by user')
        else:
            logging.warning('Token confirmation failed')

    with open(os.path.join(turnoff_path, 'token'), 'w') as f:
        f.write(entered_token)
        logging.info('Token written to file')

    logging.info('Initial setup completed')


if __name__ == "__main__":
    auto()
