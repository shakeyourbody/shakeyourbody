using System;
using Godot;
using System.Collections.Generic;

public class Play : Node
{

    private AudioStreamPlayer _Audioplayer;
    public ScoreManager Score;

    public bool Paused = false;
    private float _LastSongPosition = -1;

    public List<PathManager.TimedPathNode>[] Moves;
    public Godot.AudioStream Song;
    public List<Joint> ActiveJoints;
    private Joints _Coords;

    public override void _Ready()
    {
        OS.WindowFullscreen = true;
        Score = new ScoreManager();
        _SetupMoves();
        _SetupAudioPlayer();
        _Startgame();
    }

    private void _SetupMoves()
    {
        ActiveJoints = new List<Joint>();

        List<PathManager.TimedPathNode> noseMoves = Moves[0];
        List<PathManager.TimedPathNode> rWristMoves = Moves[1];
        List<PathManager.TimedPathNode> lWristMoves = Moves[2];

        foreach (PathManager.TimedPathNode node in noseMoves)
        {
            Joint joint = new Joint() {
                Position = node.Position,
                StartAt = node.TimeStamp - Joint.AliveForDefaul,
                JointType = Joint.Type.NOSE
            };

            joint.Connect("Expired", this, nameof(OnJointExpired));

            AddChild(joint);
            ActiveJoints.Add(joint);
        }

        foreach (PathManager.TimedPathNode node in rWristMoves)
        {
            Joint joint = new Joint() {
                Position = node.Position,
                StartAt = node.TimeStamp - Joint.AliveForDefaul,
                JointType = Joint.Type.RHAND
            };

            joint.Connect("Expired", this, nameof(OnJointExpired));

            AddChild(joint);
            ActiveJoints.Add(joint);
        }

        foreach (PathManager.TimedPathNode node in lWristMoves)
        {
            Joint joint = new Joint() {
                Position = node.Position,
                StartAt = node.TimeStamp - Joint.AliveForDefaul,
                JointType = Joint.Type.LHAND
            };

            joint.Connect("Expired", this, nameof(OnJointExpired));

            AddChild(joint);
            ActiveJoints.Add(joint);
        }
    }

    private void _SetupAudioPlayer()
    {
        // Load selected path as audio stream
        _Audioplayer = GetNode<AudioStreamPlayer>("AudioPlayer");
        _Audioplayer.Stream = Song;
    }

    private void _Startgame()
    {
        // Show joints
        _Coords = GetNode<Joints>("Joints");
        _Coords.Hidden = false;

        // Start audio player timer
        _Audioplayer.Play();
    }

    public void SetPause()
    {
        GetNode<Timebar>("Timebar").Paused = true;
        GetNode<HBoxContainer>("HUD/Margin/Center/PauseContainer").Hide();
        GetNode<HBoxContainer>("HUD/Margin/Center/PlayContainer").Show();
        _LastSongPosition = _Audioplayer.GetPlaybackPosition();
        _Audioplayer.Stop();
        Paused = true;
        foreach (Joint joint in ActiveJoints) joint.Pause();
    }

    public void SetPlay() 
    {
        GetNode<Timebar>("Timebar").Paused = false;
        GetNode<HBoxContainer>("HUD/Margin/Center/PlayContainer").Hide();
        GetNode<HBoxContainer>("HUD/Margin/Center/PauseContainer").Show();
        _Audioplayer.Play();
        _Audioplayer.Seek(_LastSongPosition);
        _LastSongPosition = -1;
        Paused = false;
        foreach (Joint joint in ActiveJoints) joint.UnPause();
    }

    public void SongEnded()
    {
        if (_LastSongPosition == -1) StopAll();
    }

    public void StopAll()
    {
        _Audioplayer.Stop();
        _ToMenu();
    }

    private void _ToMenu()
    {
        PackedScene target = GD.Load("res://Scenes/DisplayScore/DisplayScore.tscn") as PackedScene;
        DisplayScore scene = (DisplayScore) target.Instance();
        scene.Score = Math.Round(Score.Percent * 100).ToString();

        for (int i = 0; i < GetChildCount(); i += 1) GetChild(i).QueueFree();
        QueueFree();
        GetTree().Root.AddChild(scene);
    }

    public void OnJointExpired(Joint.Type type, Vector2 expected)
    {
        Vector2 real;
        switch (type)
        {
            case Joint.Type.NOSE:  real = _Coords.Nose;   break;
            case Joint.Type.RHAND: real = _Coords.RWrist; break;
            case Joint.Type.LHAND: real = _Coords.LWrist; break;
            default: real = new Vector2(); break;
        }
        Score.Step((int) real.DistanceTo(expected));
    }

}
