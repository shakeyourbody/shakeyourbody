using Godot;
using System;
using System.Net;
using System.Net.Sockets;
using System.Threading.Tasks;

public class Pose : Node
{

    [Export]
    public int CameraW = 1280;
    
    [Export]
    public int CameraH = 720;


    public struct JointsPacket {
        public Vector2 nose;
        public Vector2 rWrist;
        public Vector2 lWrist;

        public JointsPacket(byte[] buffer, int CameraW, int CameraH)
        {
            // Parse buffered c++ struct into a c# struct
            nose.x =   1 - (float) IntBitsToDouble((buffer[0]  & 0xFF) ^ (buffer[1]  & 0xFF) << 8 ^ (buffer[2]  & 0xFF) << 16 ^ (buffer[3]  & 0xFF) << 24) / CameraW;
            nose.y =       (float) IntBitsToDouble((buffer[4]  & 0xFF) ^ (buffer[5]  & 0xFF) << 8 ^ (buffer[6]  & 0xFF) << 16 ^ (buffer[7]  & 0xFF) << 24) / CameraH;
            rWrist.x = 1 - (float) IntBitsToDouble((buffer[8]  & 0xFF) ^ (buffer[9]  & 0xFF) << 8 ^ (buffer[10] & 0xFF) << 16 ^ (buffer[11] & 0xFF) << 24) / CameraW;
            rWrist.y =     (float) IntBitsToDouble((buffer[12] & 0xFF) ^ (buffer[13] & 0xFF) << 8 ^ (buffer[14] & 0xFF) << 16 ^ (buffer[15] & 0xFF) << 24) / CameraH;
            lWrist.x = 1 - (float) IntBitsToDouble((buffer[16] & 0xFF) ^ (buffer[17] & 0xFF) << 8 ^ (buffer[18] & 0xFF) << 16 ^ (buffer[19] & 0xFF) << 24) / CameraW;
            lWrist.y =     (float) IntBitsToDouble((buffer[20] & 0xFF) ^ (buffer[21] & 0xFF) << 8 ^ (buffer[22] & 0xFF) << 16 ^ (buffer[23] & 0xFF) << 24) / CameraH;
        }

        public static double IntBitsToDouble(int bits, int startIndex = 0)
        {
            // Convert an int-formatted bit serise into a double
            Byte[] bytes = BitConverter.GetBytes(bits);
            double res = BitConverter.ToSingle(bytes, startIndex);
            return res;
        }
    }

    [Export]
    public int UdpPORT = 4124;

    [Export]
    public string UdpIP = "127.0.0.1";

    private JointsPacket _LastPose;
    private bool _IsLastPoseNew = false;
    public JointsPacket LastPose {
        get {
            _IsLastPoseNew = false;
            return _LastPose;
        }
    }


    private UdpClient _UdpConnection;
    private IPEndPoint _UdpEndpoint;
    private Task _UdpConnectionRunner;
    private bool _UdpRunning = false;


    public override void _Ready()
    {
        _SetupSocket();
        _StartSocketListener();
    }

    private void _SetupSocket()
    {
        // Setup local endpoint for the socket
        IPAddress address = IPAddress.Parse(UdpIP);
        _UdpEndpoint = new IPEndPoint(address, UdpPORT);
    
        // Create UDP socket
        _UdpConnection = new UdpClient();
        _UdpConnection.Client.Bind(_UdpEndpoint);
    }

    private void _StartSocketListener()
    {
        _UdpRunning = true;
        _UdpConnectionRunner = Task.Run(() => {
            while (_UdpRunning)
            {
                // Receive buffered data from UDP and parse it
                Byte[] buffer = _UdpConnection.Receive(ref _UdpEndpoint);
                _LastPose = new JointsPacket(buffer, CameraW, CameraH);
                _IsLastPoseNew = true;
            }
        });
    }

}
