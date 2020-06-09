using Godot;
using System;

public class Joints : Node
{
    private Pose.JointsPacket _Coords;
    public Pose.JointsPacket Coords { get { return _Coords; } }

    [Export]
    public bool Hidden = false;

    public Vector2 Nose = new Vector2();
    public Vector2 RWrist = new Vector2();
    public Vector2 LWrist = new Vector2();

    public override void _Process(float delta)
    {
        _UpdatePose();
        _UpdateJoints();
    }

    private void _UpdateJoints()
    {
        // Scale joints
        Vector2 viewport = GetViewport().Size;
        Nose   = _Coords.nose   * viewport;
        RWrist = _Coords.rWrist * viewport;
        LWrist = _Coords.lWrist * viewport;

        // Move joints
        GetNode<Node2D>("Nose").Position    = Nose;
        GetNode<Node2D>("RWrist").Position  = RWrist;
        GetNode<Node2D>("LWrist").Position  = LWrist;

        Vector2 size = GetViewport().Size;

        // Hide/Show joints
        if (Hidden || Nose.x <= 0 || Nose.y <= 0 || Nose.x >= size.x || Nose.y >= size.y) GetNode<Node2D>("Nose").Hide();
        else GetNode<Node2D>("Nose").Show();
        if (Hidden || RWrist.x <= 0 || RWrist.y <= 0 || RWrist.x >= size.x || RWrist.y >= size.y) GetNode<Node2D>("RWrist").Hide();
        else GetNode<Node2D>("RWrist").Show();
        if (Hidden || LWrist.x <= 0 || LWrist.y <= 0 || LWrist.x >= size.x || LWrist.y >= size.y) GetNode<Node2D>("LWrist").Hide();
        else GetNode<Node2D>("LWrist").Show();

    }

    private void _UpdatePose()
    {
        Pose poseNode = (Pose) GetNode<Node>("Pose");
        _Coords = poseNode.LastPose;
    }
}
