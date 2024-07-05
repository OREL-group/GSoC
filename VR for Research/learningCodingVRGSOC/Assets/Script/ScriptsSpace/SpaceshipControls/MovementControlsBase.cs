using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class MovementControlsBase : IMovementControls
{
    public abstract float YawAmount { get; }
    public abstract float PitchAmount { get; }
    public abstract float RollAmount { get; }
    public abstract float ThrustAmount { get; }


}
