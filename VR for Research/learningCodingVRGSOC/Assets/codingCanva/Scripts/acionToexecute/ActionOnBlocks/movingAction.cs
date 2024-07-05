using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "NewMovingAction", menuName = "Actions/MovingAction")]
public class MovingAction : ActionBase
{
    public enum MoveDirection { None ,GoUp, GoDown, GoStraight, GoRight, GoLeft,GoBack }
    public MoveDirection moveDirection;

    public override string GetActionText()
    {
        return $"Moving Action: {moveDirection}";
    }
}

[CreateAssetMenu(fileName = "NewPrintAction", menuName = "Actions/PrintAction")]
public class PrintAction : ActionBase
{
    public string textToPrint;

    public override string GetActionText()
    {
        return $"Print Action: {textToPrint}";
    }
}

