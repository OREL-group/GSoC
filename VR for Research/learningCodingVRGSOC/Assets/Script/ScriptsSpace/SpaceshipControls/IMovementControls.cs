using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public interface IMovementControls 
{
    float YawAmount { get; }
    float PitchAmount { get; }
    float RollAmount{get; }
    float ThrustAmount {  get; }   

}
