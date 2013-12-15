//
//  Task worker in C++
//  Connects PULL socket to tcp://localhost:5557
//  Collects workloads from ventilator via that socket
//  Connects PUSH socket to tcp://localhost:5558
//  Sends results to sink via that socket
//
//  Olivier Chamoux <olivier.chamoux@fr.thalesgroup.com>
//
#include "zhelpers.hpp"
#include <fstream>

int main (int argc, char *argv[])
{
    zmq::context_t context(1);

    //  Socket to receive messages on
    zmq::socket_t receiver(context, ZMQ_PULL);
    receiver.connect("tcp://localhost:6557");

    //  Socket to send messages to
    zmq::socket_t sender(context, ZMQ_PUSH);
    sender.connect("tcp://localhost:6558");

    std::ofstream f;
    f.open ("example.txt");

    std::cout << "setup sockets" << std::endl;
    f << "setup sockets\n";

    //  Process tasks forever
    while (1) {
        std::cout << "in the wile" << std::endl;
        f << "in the wile\n";

        zmq::message_t message;
        int workload;           //  Workload in msecs

        std::cout << "waiting to receive in C" << std::endl;
        f << "waiting to receive in C\n";

        receiver.recv(&message);

        std::cout << " received in C!!" << std::endl;
        f << " received in C!!\n";

        std::istringstream iss(static_cast<char*>(message.data()));
        iss >> workload;

        //  Do the work
        s_sleep(workload);
        std::cout << "worked" << std::endl;
        f << "worked\n";

        //  Send results to sink
        message.rebuild();
        sender.send(message);

        //  Simple progress indicator for the viewer
        std::cout << "." << std::flush;
        f << ".";
    }
    f.close();
    return 0;
}
