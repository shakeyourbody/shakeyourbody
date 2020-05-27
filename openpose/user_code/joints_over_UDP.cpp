#define OPENPOSE_FLAGS_DISABLE_DISPLAY

#include <opencv2/opencv.hpp>
#include <openpose/flags.hpp>
#include <openpose/headers.hpp>

#include "Packet.h"
#include "socket/UdpSocket.h"
#include "default.h"

// Flags
DEFINE_bool(no_display, false, "enable to disable visual display");

bool display(std::shared_ptr<std::vector<std::shared_ptr<op::Datum>>>& datum) {
  if (datum != nullptr && !datum->empty()) {
    const cv::Mat mat = OP_OP2CVCONSTMAT(datum->at(0)->cvOutputData);
    cv::imshow(OPEN_POSE_NAME_AND_VERSION + " - JOINTS OVER UDP", mat);
  } else op::opLog("nullptr or empty datum found", op::Priority::High);
  const auto key = (char)cv::waitKey(1);
  return (key == 27); // exit with `Esc`
}

void jointsOverUDP(const std::shared_ptr<std::vector<std::shared_ptr<op::Datum>>>& datum) {
  const auto& poseKeypoints = datum->at(0)->poseKeypoints;

  PosePacket packet;
  iit::sock::UdpSocket<PosePacket> UDPSocket;

  if (poseKeypoints.getSize(0)) {
    for (int i = 0; i < 2; i += 1) {
      packet.Nose[i] = poseKeypoints[{0, 0, i}];
      packet.Neck[i] = poseKeypoints[{0, 1, i}];
      packet.RShoulder[i] = poseKeypoints[{0, 2, i}];
      packet.RElbow[i] = poseKeypoints[{0, 3, i}];
      packet.RWrist[i] = poseKeypoints[{0, 4, i}];
      packet.LShoulder[i] = poseKeypoints[{0, 5, i}];
      packet.LElbow[i] = poseKeypoints[{0, 6, i}];
      packet.LWrist[i] = poseKeypoints[{0, 7, i}];
      packet.MidHip[i] = poseKeypoints[{0, 8, i}];
      packet.RHip[i] = poseKeypoints[{0, 9, i}];
      packet.RKnee[i] = poseKeypoints[{0, 10, i}];
      packet.RAnkle[i] = poseKeypoints[{0, 11, i}];
      packet.LHip[i] = poseKeypoints[{0, 12, i}];
      packet.LKnee[i] = poseKeypoints[{0, 13, i}];
      packet.LAnkle[i] = poseKeypoints[{0, 14, i}];
      packet.REye[i] = poseKeypoints[{0, 15, i}];
      packet.LEye[i] = poseKeypoints[{0, 16, i}];
      packet.REar[i] = poseKeypoints[{0, 17, i}];
      packet.LEar[i] = poseKeypoints[{0, 18, i}];
      packet.LBigToe[i] = poseKeypoints[{0, 19, i}];
      packet.LSmallToe[i] = poseKeypoints[{0, 20, i}];
      packet.LHeel[i] = poseKeypoints[{0, 21, i}];
      packet.RBigToe[i] = poseKeypoints[{0, 22, i}];
      packet.RSmallToe[i] = poseKeypoints[{0, 23, i}];
      packet.RHeel[i] = poseKeypoints[{0, 24, i}];
    }
    UDPSocket.sock_send(packet);
  }
}

int main(int argc, char* argv[]) {
  gflags::ParseCommandLineFlags(&argc, &argv, true);

  op::opLog("starting wrapper", op::Priority::High);
  op::Wrapper wrapper{op::ThreadManagerMode::AsynchronousOut};
  configureWrapper(wrapper);
  wrapper.start();

  bool looping = true;
  while (looping) {
    std::shared_ptr<std::vector<std::shared_ptr<op::Datum>>> datum;
    if (wrapper.waitAndPop(datum)) {
      if (!FLAGS_no_display) looping = !display(datum);
      // else op::opLog(".", op::Priority::High);
      jointsOverUDP(datum);
    } else if (!wrapper.isRunning()) looping = false;
    else op::opLog("processed daatum could not be emplaced", op::Priority::High);
  }

  op::opLog("stopping wrapper", op::Priority::High);
  wrapper.stop();

  return 0;
}