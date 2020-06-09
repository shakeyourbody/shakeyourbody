using Godot;
using System;

public class Timebar : Control
{

    [Export]
    public string AudioStreamPath;
    private AudioStreamPlayer _AudioStream;
    private float _Percent = 0;

    [Export]
    public bool Paused = false;

    private Color _ColorPlaying = new Color(251f/256f, 72f/256f, 73f/256f);
    private Color _ColorPaused = new Color(3f/256f, 122f/256f, 144f/256f);

    public override void _Ready()
    {
        _AudioStream = GetParent().GetNode<AudioStreamPlayer>(AudioStreamPath);
    }

    public override void _Process(float delta)
    {
        if (_AudioStream.Playing) { _Percent = _AudioStream.GetPlaybackPosition() / _AudioStream.Stream.GetLength(); }
        Update();
    }

    public override void _Draw()
    {
        Vector2 viewport = GetViewport().Size;
        Rect2 bar = new Rect2(new Vector2(), new Vector2(_Percent * viewport.x, 10));
        DrawRect(bar, (Paused) ? _ColorPaused : _ColorPlaying);
    }

}
