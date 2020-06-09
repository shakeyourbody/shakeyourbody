using System;
using Godot;

public class ScoreVis : Control
{
    private double _Percent;

    private Color _ColorBorder = new Color(255f/256f, 107f/256f, 0f/256f);
    private Color _ColorMain = new Color(255f/256f, 216f/256f, 61f/256f);

    private int _BorderSize = 2;
    private int _Width = 10;
    private int _DistX = 40;
    private int _DistY = 80;

    public override void _Ready()
    {
        
    }

    public override void _Process(float delta)
    {
        Play parent = (Play) GetParent();
        _Percent = parent.Score.Percent;
        if (Double.IsNaN(_Percent)) _Percent = 0;
        Update();
    }

    public override void _Draw()
    {
        Vector2 viewport = GetViewport().Size;

        float h = (float) _Percent * (viewport.y - 2 * _DistY - 10) + 10;
        float y = (viewport.y - _DistY) - h;

        Vector2 position = new Vector2(viewport.x - _DistX - _Width, y);
        Vector2 size = new Vector2(10, h);

        Vector2 positionBorders = new Vector2(viewport.x - _DistX - _Width - _BorderSize,   _DistY - _BorderSize);
        Vector2 sizeBorders = new Vector2(_Width + 2 * _BorderSize, viewport.y - 2 * _DistY + 2 * _BorderSize);

        Rect2 main = new Rect2(position, size);
        Rect2 border = new Rect2(positionBorders, sizeBorders);

        DrawRect(border, _ColorBorder);
        DrawRect(main, _ColorMain);
    }

}
