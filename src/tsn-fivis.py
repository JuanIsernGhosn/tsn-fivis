from systemconfigurer import ApplicationConfigurer, Application
import time
import argparse


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main(args):

    api_config_file = args.apiconfig
    log_folder = args.logfolder
    simulate = args.simulate
    app_configurer = ApplicationConfigurer(api_config_file, log_folder, simulate)
    app = Application(args.time_between_measure, args.send_every)
    handlers = app_configurer.getNodeHandlers()
    app.addHandlers(handlers)
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
                        default="../res/logs/",
                        help='Path of the folder with the TSN node logs')
    parser.add_argument('--api_config', dest='apiconfig', type=str,
                        default="../res/api_configuration.json",
                        help='Path of the .json file with the Fivis api configuration')
    parser.add_argument('--time_between_measure', default=5, type=float,
                        help='Interval of measurements in seconds')
    parser.add_argument('--send_every', default=1, type=int,
                        help='Number of measures before sending it to FIVIS')
    parser.add_argument("--simulate", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Activate nice mode.")

    args = parser.parse_args()
    main(args)
