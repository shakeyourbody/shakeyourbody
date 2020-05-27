// ------------------------- OpenPose C++ API Tutorial - Example 11 - Custom Output -------------------------
// Asynchronous mode: ideal for fast prototyping when performance is not an issue.
// In this function, the user can implement its own way to render/display/storage the results.

// Third-party dependencies
#include <opencv2/opencv.hpp>
// Command-line user interface
#define OPENPOSE_FLAGS_DISABLE_DISPLAY
#include <openpose/flags.hpp>
// OpenPose dependencies
#include <openpose/headers.hpp>

#include "socket/UdpSocket.h"
// #include "Packet.h"
#include "Packet.h"

// Custom OpenPose flags
// Display
DEFINE_bool(no_display,                 false,
    "Enable to disable the visual display.");

// This worker will just read and return all the jpg files in a directory
class UserOutputClass
{
public:

    UserOutputClass()
    {
//        udpSocket_ = std::make_shared<iit::sock::UdpSocket<op::PosePacket>>();
        udpSocket_.sock_init();
        udpSocket_.sock_connect("127.0.0.1", 4124);
    }

    bool display(const std::shared_ptr<std::vector<std::shared_ptr<op::Datum>>>& datumsPtr)
    {
        // User's displaying/saving/other processing here
            // datumPtr->cvOutputData: rendered frame with pose or heatmaps
            // datumPtr->poseKeypoints: Array<float> with the estimated pose
        if (datumsPtr != nullptr && !datumsPtr->empty())
        {
            // Display image and sleeps at least 1 ms (it usually sleeps ~5-10 msec to display the image)
            const cv::Mat cvMat = OP_OP2CVCONSTMAT(datumsPtr->at(0)->cvOutputData);
            cv::imshow(OPEN_POSE_NAME_AND_VERSION + " - Tutorial C++ API", cvMat);
        }
        else
            op::opLog("Nullptr or empty datumsPtr found.", op::Priority::High);
        const auto key = (char)cv::waitKey(1);
        return (key == 27);
    }

    void printKeypoints(const std::shared_ptr<std::vector<std::shared_ptr<op::Datum>>>& datumsPtr)
    {
        // Example: How to use the pose keypoints
        if (datumsPtr != nullptr && !datumsPtr->empty())
        {
            // Accesing each element of the keypoints
            const auto& poseKeypoints = datumsPtr->at(0)->poseKeypoints;
            // op::opLog("+++++++++++++++++++++");
            // std::vector<int> parts = {0, 4, 7}; //Nose, RWrist, LWrist

            // for (const auto& part : parts)
            // {
            //     std::string valueToPrint;
            //     for (auto xyscore = 0; xyscore < poseKeypoints.getSize(2); xyscore++) {
            //         valueToPrint += std::to_string(poseKeypoints[{0, part, xyscore}]) + " ";
            //     }
            //     op::opLog(valueToPrint);
            // }
            // op::opLog("---------------------");

            // if (poseKeypoints.getSize(0))
            // {

            //     packet_.twoD_cord_nose[0] = poseKeypoints[{0, parts[0], 0}];
            //     packet_.twoD_cord_nose[1] = poseKeypoints[{0, parts[0], 1}];
            //     packet_.twoD_cord_r_wrist[0] = poseKeypoints[{0, parts[1], 0}];
            //     packet_.twoD_cord_r_wrist[1] = poseKeypoints[{0, parts[1], 1}];
            //     packet_.twoD_cord_l_wrist[0] = poseKeypoints[{0, parts[2], 0}];
            //     packet_.twoD_cord_l_wrist[1] = poseKeypoints[{0, parts[2], 1}];

            //     udpSocket_.sock_send(packet_);
            // }

            if (poseKeypoints.getSize(0))
            {
                for (int _i_ = 0; _i_ < 2; _i_ += 1)
                {
                    packet_.Nose[_i_] = poseKeypoints[{0, 0, _i_}];
                    packet_.Neck[_i_] = poseKeypoints[{0, 1, _i_}];
                    packet_.RShoulder[_i_] = poseKeypoints[{0, 2, _i_}];
                    packet_.RElbow[_i_] = poseKeypoints[{0, 3, _i_}];
                    packet_.RWrist[_i_] = poseKeypoints[{0, 4, _i_}];
                    packet_.LShoulder[_i_] = poseKeypoints[{0, 5, _i_}];
                    packet_.LElbow[_i_] = poseKeypoints[{0, 6, _i_}];
                    packet_.LWrist[_i_] = poseKeypoints[{0, 7, _i_}];
                    packet_.MidHip[_i_] = poseKeypoints[{0, 8, _i_}];
                    packet_.RHip[_i_] = poseKeypoints[{0, 9, _i_}];
                    packet_.RKnee[_i_] = poseKeypoints[{0, 10, _i_}];
                    packet_.RAnkle[_i_] = poseKeypoints[{0, 11, _i_}];
                    packet_.LHip[_i_] = poseKeypoints[{0, 12, _i_}];
                    packet_.LKnee[_i_] = poseKeypoints[{0, 13, _i_}];
                    packet_.LAnkle[_i_] = poseKeypoints[{0, 14, _i_}];
                    packet_.REye[_i_] = poseKeypoints[{0, 15, _i_}];
                    packet_.LEye[_i_] = poseKeypoints[{0, 16, _i_}];
                    packet_.REar[_i_] = poseKeypoints[{0, 17, _i_}];
                    packet_.LEar[_i_] = poseKeypoints[{0, 18, _i_}];
                    packet_.LBigToe[_i_] = poseKeypoints[{0, 19, _i_}];
                    packet_.LSmallToe[_i_] = poseKeypoints[{0, 20, _i_}];
                    packet_.LHeel[_i_] = poseKeypoints[{0, 21, _i_}];
                    packet_.RBigToe[_i_] = poseKeypoints[{0, 22, _i_}];
                    packet_.RSmallToe[_i_] = poseKeypoints[{0, 23, _i_}];
                    packet_.RHeel[_i_] = poseKeypoints[{0, 24, _i_}];
                }

                udpSocket_.sock_send(packet_);
            }

        }
        else
            op::opLog("Nullptr or empty datumsPtr found.", op::Priority::High);
    }

private:

    iit::sock::UdpSocket<PosePacket> udpSocket_;
    PosePacket packet_;
};

void configureWrapper(op::Wrapper& opWrapper)
{
    try
    {
        // Configuring OpenPose

        // logging_level
        op::checkBool(
            0 <= FLAGS_logging_level && FLAGS_logging_level <= 255, "Wrong logging_level value.",
            __LINE__, __FUNCTION__, __FILE__);
        op::ConfigureLog::setPriorityThreshold((op::Priority)FLAGS_logging_level);
        op::Profiler::setDefaultX(FLAGS_profile_speed);

        // Applying user defined configuration - GFlags to program variables
        // producerType
        op::ProducerType producerType;
        op::String producerString;
        std::tie(producerType, producerString) = op::flagsToProducer(
            op::String(FLAGS_image_dir), op::String(FLAGS_video), op::String(FLAGS_ip_camera), FLAGS_camera,
            FLAGS_flir_camera, FLAGS_flir_camera_index);
        // cameraSize
        const auto cameraSize = op::flagsToPoint(op::String(FLAGS_camera_resolution), "-1x-1");
        // outputSize
        const auto outputSize = op::flagsToPoint(op::String(FLAGS_output_resolution), "-1x-1");
        // netInputSize
        const auto netInputSize = op::flagsToPoint(op::String(FLAGS_net_resolution), "-1x368");
        // faceNetInputSize
        const auto faceNetInputSize = op::flagsToPoint(op::String(FLAGS_face_net_resolution), "368x368 (multiples of 16)");
        // handNetInputSize
        const auto handNetInputSize = op::flagsToPoint(op::String(FLAGS_hand_net_resolution), "368x368 (multiples of 16)");
        // poseMode
        const auto poseMode = op::flagsToPoseMode(FLAGS_body);
        // poseModel
        const auto poseModel = op::flagsToPoseModel(op::String(FLAGS_model_pose));
        // JSON saving
        if (!FLAGS_write_keypoint.empty())
            op::opLog(
                "Flag `write_keypoint` is deprecated and will eventually be removed. Please, use `write_json`"
                " instead.", op::Priority::Max);
        // keypointScaleMode
        const auto keypointScaleMode = op::flagsToScaleMode(FLAGS_keypoint_scale);
        // heatmaps to add
        const auto heatMapTypes = op::flagsToHeatMaps(FLAGS_heatmaps_add_parts, FLAGS_heatmaps_add_bkg,
                                                      FLAGS_heatmaps_add_PAFs);
        const auto heatMapScaleMode = op::flagsToHeatMapScaleMode(FLAGS_heatmaps_scale);
        // >1 camera view?
        const auto multipleView = (FLAGS_3d || FLAGS_3d_views > 1 || FLAGS_flir_camera);
        // Face and hand detectors
        const auto faceDetector = op::flagsToDetector(FLAGS_face_detector);
        const auto handDetector = op::flagsToDetector(FLAGS_hand_detector);
        // Enabling Google Logging
        const bool enableGoogleLogging = true;

        // Pose configuration (use WrapperStructPose{} for default and recommended configuration)
        const op::WrapperStructPose wrapperStructPose{
            poseMode, netInputSize, outputSize, keypointScaleMode, FLAGS_num_gpu, FLAGS_num_gpu_start,
            FLAGS_scale_number, (float)FLAGS_scale_gap, op::flagsToRenderMode(FLAGS_render_pose, multipleView),
            poseModel, !FLAGS_disable_blending, (float)FLAGS_alpha_pose, (float)FLAGS_alpha_heatmap,
            FLAGS_part_to_show, op::String(FLAGS_model_folder), heatMapTypes, heatMapScaleMode, FLAGS_part_candidates,
            (float)FLAGS_render_threshold, FLAGS_number_people_max, FLAGS_maximize_positives, FLAGS_fps_max,
            op::String(FLAGS_prototxt_path), op::String(FLAGS_caffemodel_path),
            (float)FLAGS_upsampling_ratio, enableGoogleLogging};
        opWrapper.configure(wrapperStructPose);
        // Face configuration (use op::WrapperStructFace{} to disable it)
        const op::WrapperStructFace wrapperStructFace{
            FLAGS_face, faceDetector, faceNetInputSize,
            op::flagsToRenderMode(FLAGS_face_render, multipleView, FLAGS_render_pose),
            (float)FLAGS_face_alpha_pose, (float)FLAGS_face_alpha_heatmap, (float)FLAGS_face_render_threshold};
        opWrapper.configure(wrapperStructFace);
        // Hand configuration (use op::WrapperStructHand{} to disable it)
        const op::WrapperStructHand wrapperStructHand{
            FLAGS_hand, handDetector, handNetInputSize, FLAGS_hand_scale_number, (float)FLAGS_hand_scale_range,
            op::flagsToRenderMode(FLAGS_hand_render, multipleView, FLAGS_render_pose), (float)FLAGS_hand_alpha_pose,
            (float)FLAGS_hand_alpha_heatmap, (float)FLAGS_hand_render_threshold};
        opWrapper.configure(wrapperStructHand);
        // Extra functionality configuration (use op::WrapperStructExtra{} to disable it)
        const op::WrapperStructExtra wrapperStructExtra{
            FLAGS_3d, FLAGS_3d_min_views, FLAGS_identification, FLAGS_tracking, FLAGS_ik_threads};
        opWrapper.configure(wrapperStructExtra);
        // Producer (use default to disable any input)
        const op::WrapperStructInput wrapperStructInput{
            producerType, producerString, FLAGS_frame_first, FLAGS_frame_step, FLAGS_frame_last,
            FLAGS_process_real_time, FLAGS_frame_flip, FLAGS_frame_rotate, FLAGS_frames_repeat,
            cameraSize, op::String(FLAGS_camera_parameter_path), FLAGS_frame_undistort, FLAGS_3d_views};
        opWrapper.configure(wrapperStructInput);
        // Output (comment or use default argument to disable any output)
        const op::WrapperStructOutput wrapperStructOutput{
            FLAGS_cli_verbose, op::String(FLAGS_write_keypoint), op::stringToDataFormat(FLAGS_write_keypoint_format),
            op::String(FLAGS_write_json), op::String(FLAGS_write_coco_json), FLAGS_write_coco_json_variants,
            FLAGS_write_coco_json_variant, op::String(FLAGS_write_images), op::String(FLAGS_write_images_format),
            op::String(FLAGS_write_video), FLAGS_write_video_fps, FLAGS_write_video_with_audio,
            op::String(FLAGS_write_heatmaps), op::String(FLAGS_write_heatmaps_format), op::String(FLAGS_write_video_3d),
            op::String(FLAGS_write_video_adam), op::String(FLAGS_write_bvh), op::String(FLAGS_udp_host),
            op::String(FLAGS_udp_port)};
        opWrapper.configure(wrapperStructOutput);
        // No GUI. Equivalent to: opWrapper.configure(op::WrapperStructGui{});
        // Set to single-thread (for sequential processing and/or debugging and/or reducing latency)
        if (FLAGS_disable_multi_thread)
            opWrapper.disableMultiThreading();
    }
    catch (const std::exception& e)
    {
        op::error(e.what(), __LINE__, __FUNCTION__, __FILE__);
    }
}

int tutorialApiCpp()
{
    try
    {
        op::opLog("Starting OpenPose demo...", op::Priority::High);
        const auto opTimer = op::getTimerInit();

        // Configuring OpenPose
        op::opLog("Configuring OpenPose...", op::Priority::High);
        op::Wrapper opWrapper{op::ThreadManagerMode::AsynchronousOut};
        configureWrapper(opWrapper);

        // Start, run, and stop processing - exec() blocks this thread until OpenPose wrapper has finished
        op::opLog("Starting thread(s)...", op::Priority::High);
        opWrapper.start();

        // User processing
        UserOutputClass userOutputClass;
        bool userWantsToExit = false;
        while (!userWantsToExit)
        {
            // Pop frame
            std::shared_ptr<std::vector<std::shared_ptr<op::Datum>>> datumProcessed;
            if (opWrapper.waitAndPop(datumProcessed))
            {
                if (!FLAGS_no_display) //camera
                    userWantsToExit = userOutputClass.display(datumProcessed);;
                userOutputClass.printKeypoints(datumProcessed);
            }
            // If OpenPose finished reading images
            else if (!opWrapper.isRunning())
                break;
            // Something else happened
            else
                op::opLog("Processed datum could not be emplaced.", op::Priority::High);
        }

        op::opLog("Stopping thread(s)", op::Priority::High);
        opWrapper.stop();

        // Measuring total time
        op::printTime(opTimer, "OpenPose demo successfully finished. Total time: ", " seconds.", op::Priority::High);

        // Return
        return 0;
    }
    catch (const std::exception&)
    {
        return -1;
    }
}

int main(int argc, char *argv[])
{
    // Parsing command line flags
    gflags::ParseCommandLineFlags(&argc, &argv, true);

    // Running tutorialApiCpp
    return tutorialApiCpp();
}
