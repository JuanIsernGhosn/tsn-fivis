from systemconfigurer import ApplicationConfigurer, Application
import time
import argparse


def main(args):

    api_config_file = args.apiconfig
    log_folder = args.logfolder
    app_configurer = ApplicationConfigurer(api_config_file, log_folder)
    app = Application(args.time_between_measure, args.send_every)
    app.addHandlers(app_configurer.geNodeHandlers())
    app.start()

    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        app.stop()
        app.join()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Record and send TSN data to FIVIS')
    parser.add_argument('--log_folder', dest='logfolder', type=str,
                        default="../res/TSN_logs/",
                        help='Path of the folder with the TSN node logs')
    parser.add_argument('--api_config', dest='apiconfig', type=str,
                        default="../res/api_configuration.json",
                        help='Path of the .json file with the Fivis api configuration')
    parser.add_argument('--time_between_measure', default=5, type=float,
                        help='Interval of measurements in seconds')
    parser.add_argument('--send_every', default=1, type=int,
                        help='Number of measures before sending it to FIVIS')

    args = parser.parse_args()
    main(args)
