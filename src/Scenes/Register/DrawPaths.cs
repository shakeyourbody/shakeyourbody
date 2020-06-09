using Godot;
using System.Collections.Generic;

public class DrawPaths : Node
{
    
    private List<Joint> _ActiveJoints;

    public override void _Ready()
    {
        _ActiveJoints = new List<Joint>();
    }

    public void Add(Vector2 position, float aliveFor = 1, Joint.Type type = Joint.Type.NOSE)
    {
        Joint joint = new Joint() {
            Position = position,
            AliveFor = aliveFor,
            StartAt = 0,
            JointType = type
        };

        AddChild(joint);
        _ActiveJoints.Add(joint);
    }

    public void Pause()
    {
        foreach (Joint joint in _ActiveJoints) joint.Pause();
    }

    public void UnPause()
    {
        foreach (Joint joint in _ActiveJoints) joint.UnPause();
    }

}
