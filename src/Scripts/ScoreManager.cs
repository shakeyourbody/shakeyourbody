using System.Runtime.InteropServices;
using System;

public class ScoreManager
{

    public double Score;
    public double PartialFullScore;
    public double Multiplier;
    public double PartialFullMultiplier;

    public double Percent {
        get {
            double p = Score / PartialFullScore;
            return (Double.IsNaN(p)) ? 0 : p;
        }
    }

    public enum HitType
    {
        HIT = 40, NEARLY = 80, MISS
    }

    public static (double score, Func<double, double> multiplier) Modifiers(HitType type)
    {
        switch (type)
        {
            case HitType.HIT:
                return (1, mpm => mpm + 0.1);
            case HitType.NEARLY:
                return (0.5, mpm => mpm);
            case HitType.MISS:
                return (0, mpm => 0);
            default:
                return (0, mpm => mpm);
        }
    }

    public static double FullScore(int nJoints)
    {
        ScoreManager sm = new ScoreManager();
        for (int i = 0; i < nJoints; i += 1) sm.Step(0);
        return sm.Score;
    }

    public ScoreManager()
    {
        Score = 0;
        Multiplier = 1;
        PartialFullScore = 0;
        PartialFullMultiplier = 0;
    }

    public void Step(int dist)
    {
        if (dist < (int) HitType.HIT)
        {
            var modifiers = Modifiers(HitType.HIT);
            Score += modifiers.score;
            Multiplier = modifiers.multiplier(Multiplier);
        }
        else if (dist < (int) HitType.NEARLY)
        {
            var modifiers = Modifiers(HitType.NEARLY);
            Score += modifiers.score;
            Multiplier = modifiers.multiplier(Multiplier);
        }
        else
        {
            var modifiers = Modifiers(HitType.MISS);
            Score += modifiers.score;
            Multiplier = modifiers.multiplier(Multiplier);
        }
        
        var partialFullModifiers = Modifiers(HitType.HIT);
        PartialFullScore += partialFullModifiers.score;
        PartialFullMultiplier = partialFullModifiers.multiplier(PartialFullMultiplier);
    }

}