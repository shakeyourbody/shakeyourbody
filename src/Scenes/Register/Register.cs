using System.Collections.Generic;
using Godot;

public class Register : Node
{

    private AudioStreamPlayer _Audioplayer;
    public bool Paused = false;
    private float _LastSongPosition = -1;

    [Export]
    public string SongPath;

    private float _Clock = 0;
    private List<PathManager.TimedPathNode> _NoseMoves;
    private List<PathManager.TimedPathNode> _RWristMoves;
    private List<PathManager.TimedPathNode> _LWristMoves;
    private Joints _Coords;

    public override void _Ready()
    {
        OS.WindowFullscreen = true;
        _SetupAudioPlayer();
        _Startgame();
    }

    public override void _Process(float delta)
    {
        if (!Paused)
        {
            _Clock += delta;
            GD.Print(delta);
            if (_Clock >= 3)
            {
                _NoseMoves.Add(new PathManager.TimedPathNode(_Coords.Nose, _Clock));
                _RWristMoves.Add(new PathManager.TimedPathNode(_Coords.RWrist, _Clock));
                _LWristMoves.Add(new PathManager.TimedPathNode(_Coords.LWrist, _Clock));
            }
        }

        _DrawPaths();
    }

    private void _SetupAudioPlayer()
    {
        // Load selected path as audio stream
        _Audioplayer = GetNode<AudioStreamPlayer>("AudioPlayer");
        _Audioplayer.Stream = SongsManager.AudioBufferFromFile(SongPath) as Godot.AudioStream;
    }

    private void _Startgame()
    {
        // Show joints
        _Coords = GetNode<Joints>("Joints");
        _Coords.Hidden = false;

        // Start audio player
        _Audioplayer.Play();

        _Clock = 0;
        _NoseMoves = new List<PathManager.TimedPathNode>();
        _RWristMoves = new List<PathManager.TimedPathNode>();
        _LWristMoves = new List<PathManager.TimedPathNode>();
    }

    private void _DrawPaths()
    {
        if (! HasNode("DrawPaths")) return;
        DrawPaths pathDrawer = GetNode<DrawPaths>("DrawPaths");
        pathDrawer.Add(_Coords.Nose, 1, Joint.Type.NOSE);
        pathDrawer.Add(_Coords.RWrist, 1, Joint.Type.RHAND);
        pathDrawer.Add(_Coords.LWrist, 1, Joint.Type.LHAND);
    }

    public void SetPause()
    {
        GetNode<Timebar>("Timebar").Paused = true;
        GetNode<HBoxContainer>("HUD/Margin/Center/PauseContainer").Hide();
        GetNode<HBoxContainer>("HUD/Margin/Center/PlayContainer").Show();
        _LastSongPosition = _Audioplayer.GetPlaybackPosition();
        _Audioplayer.Stop();
        Paused = true;
        // GetNode<DrawPaths>("DrawPaths").Pause();
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
        // GetNode<DrawPaths>("DrawPaths").UnPause();
    }

    public void SongEnded()
    {
        if (_LastSongPosition == -1) StopAll();
        _Save();
    }

    private void _Save()
    {
        string title = System.IO.Path.GetFileNameWithoutExtension(SongPath);

        _NoseMoves = new PathManager(_NoseMoves).Simplify().Nodes;
        _RWristMoves = new PathManager(_RWristMoves).Simplify().Nodes;
        _LWristMoves = new PathManager(_LWristMoves).Simplify().Nodes;

        List<PathManager.TimedPathNode>[] moves = new List<PathManager.TimedPathNode>[] { _NoseMoves, _RWristMoves, _LWristMoves };
        SongsManager.Serialize(title, SongPath, moves);
    }

    public void StopAll()
    {
        _Audioplayer.Stop();
        _ToMenu();
    }

    private void _ToMenu()
    {
        for (int i = 0; i < GetChildCount(); i += 1) GetChild(i).QueueFree();
        QueueFree();
        GetTree().ChangeScene("res://Scenes/Menu/Menu.tscn");
    }

}
