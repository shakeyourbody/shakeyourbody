using Godot;
using System;

public class Joint : Node2D
{

    [Signal]
    public delegate void Expired(Type type, Vector2 position);

    public enum Type { NOSE, LHAND, RHAND }

    [Export]
    public Color NoseColor = new Color(183f/256f, 154f/256f, 253f/256f, 0.2f);

    [Export]
    public Color LHandColor = new Color(19f/256f, 202f/256f, 145f/256f, 0.2f);

    [Export]
    public Color RHandColor = new Color(255f/256f, 34f/256f, 129f/256f, 0.2f);

    [Export]
    public Type JointType;

    [Export]
    public double StartAt;
    

    public static double AliveForDefaul = 2;
    public double AliveFor;

    [Export]
    public double InitialRadius = 15;

    public bool Paused = false;

    private Timer _StartTimer;
    private Timer _AliveTimer;
    private float _Percent = 1;


    public override void _Ready()
    {
        // Hide();
        AliveFor = AliveForDefaul;
        LoadChilds();
    }

    public void LoadChilds()
    {
        _AliveTimer = new Timer();
        _AliveTimer.WaitTime = (float) AliveFor;
        _AliveTimer.OneShot = true;
        _AliveTimer.Connect("timeout", this, nameof(OnAliveTimerTimeout));

        if (StartAt > 0)
        {
            _StartTimer = new Timer();
            _StartTimer.Connect("timeout", this, nameof(OnStartTimerTimeout));
            _StartTimer.WaitTime = (float) StartAt;
            _StartTimer.OneShot = true;
            AddChild(_StartTimer);
            _StartTimer.Start();
        }
        else OnStartTimerTimeout();
    }

    public void OnStartTimerTimeout()
    {
        Show();
        AddChild(_AliveTimer);
        _AliveTimer.Start();
    }

    public void OnAliveTimerTimeout()
    {
        Die();
    }

    public override void _Process(float delta)
    {
        if (!Paused && _AliveTimer.TimeLeft != _AliveTimer.WaitTime && _AliveTimer.TimeLeft >= 0)
        {
            _Percent = _AliveTimer.TimeLeft / _AliveTimer.WaitTime;
        }
    
        Update();
    }

    public override void _Draw()
    {
        Color color = new Color(0, 0, 0);
        if (JointType == Type.NOSE) color = NoseColor;
        else if (JointType == Type.LHAND) color = LHandColor;
        else if (JointType == Type.RHAND) color = RHandColor;

        // DrawArc(new Vector2(), (float) InitialRadius * _Percent, 0, Mathf.Pi * 2, 100, color, InitialRadius);
        DrawCircle(new Vector2(), (float) InitialRadius * _Percent, color);
    }

    public void Pause()
    {
        Paused = true;
        if (_StartTimer != null) _StartTimer.Paused = true;
        _AliveTimer.Paused = true;
    }

    public void UnPause()
    {
        Paused = false;
        if (_StartTimer != null) _StartTimer.Paused = false;
        _AliveTimer.Paused = false;
    }

    public void Die()
    {
        Hide();
        EmitSignal(nameof(Expired), JointType, Position);
        QueueFree();
    }

}
