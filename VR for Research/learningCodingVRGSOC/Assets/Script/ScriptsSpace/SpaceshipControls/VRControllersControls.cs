using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public class VRControllersControls : MovementControlsBase
{
    [SerializeField] float _deadZoneRadius = 0.1f;
    //float Vector2 ScreenCenter => new Vector2(Scre)

    public override float YawAmount => throw new System.NotImplementedException();

    public override float PitchAmount => throw new System.NotImplementedException();

    public override float RollAmount => throw new System.NotImplementedException();

    public override float ThrustAmount => throw new System.NotImplementedException();

   
}
