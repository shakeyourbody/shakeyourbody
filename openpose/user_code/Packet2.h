#ifndef OPENPOSE_PACKET_H
#define OPENPOSE_PACKET_H

// {0,  "Nose"},
// {1,  "Neck"},
// {2,  "RShoulder"},
// {3,  "RElbow"},
// {4,  "RWrist"},
// {5,  "LShoulder"},
// {6,  "LElbow"},
// {7,  "LWrist"},
// {8,  "MidHip"},
// {9,  "RHip"},
// {10, "RKnee"},
// {11, "RAnkle"},
// {12, "LHip"},
// {13, "LKnee"},
// {14, "LAnkle"},
// {15, "REye"},
// {16, "LEye"},
// {17, "REar"},
// {18, "LEar"},
// {19, "LBigToe"},
// {20, "LSmallToe"},
// {21, "LHeel"},
// {22, "RBigToe"},
// {23, "RSmallToe"},
// {24, "RHeel"},
// {25, "Background"}

typedef struct
{
    float Nose[2];
    float Neck[2];
    float RShoulder[2];
    float RElbow[2];
    float RWrist[2];
    float LShoulder[2];
    float LElbow[2];
    float LWrist[2];
    float MidHip[2];
    float RHip[2];
    float RKnee[2];
    float RAnkle[2];
    float LHip[2];
    float LKnee[2];
    float LAnkle[2];
    float REye[2];
    float LEye[2];
    float REar[2];
    float LEar[2];
    float LBigToe[2];
    float LSmallToe[2];
    float LHeel[2];
    float RBigToe[2];
    float RSmallToe[2];
    float RHeel[2];
} PosePacket;

#endif // OPENPOSE_PACKET_H
