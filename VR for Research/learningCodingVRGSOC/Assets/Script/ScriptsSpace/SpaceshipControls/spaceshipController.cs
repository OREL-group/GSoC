using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class spaceshipController : MonoBehaviour
{
    /*
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
        Vector3 speedThrust = Vector3.zero;
    Vector3 speedPitch = Vector3.zero;
    Vector3 speedRoll = Vector3.zero;
    Vector3 speedYaw = Vector3.zero;
    */

    [SerializeField] [Range(1000f, 10000f)]
    float _thrustForce = 7500f, 
        _pitchForce = 6000f,
        _rollForce = 1000f,
        _yawForce =2000f;

    Rigidbody _rigidBody;
    ParticleSystem particleSystem;
    ParticleSystem.VelocityOverLifetimeModule velocityModule;
    [SerializeField]
    [Range(-10f, 10f)]
    float _thrustAmount = 0f;
    [SerializeField] [Range(-1f,1f)]
    float _pitchAmount, _rollAmount, _yawAmount = 0f;

    private void Awake()
    {
        _rigidBody = GetComponent<Rigidbody>();
        if (particleSystem == null)
        {
            particleSystem = GetComponent<ParticleSystem>();
        }
        
        velocityModule = particleSystem.velocityOverLifetime;
        velocityModule.enabled = true;
    }

    private void FixedUpdate()
    {
        

        // Apply pitch torque
        if (!Mathf.Approximately(0f, _pitchAmount))
        {
            _rigidBody.AddTorque(transform.right * (_pitchForce * _pitchAmount * Time.fixedDeltaTime));
            
        }

        // Apply yaw torque
        if (!Mathf.Approximately(0f, _yawAmount))

        {
            _rigidBody.AddTorque(transform.up * (_yawForce * _yawAmount * Time.fixedDeltaTime));
        }

        // Apply roll torque
        if (!Mathf.Approximately(0f, _rollAmount))
        {
            //speedRoll = transform.forward * (_rollForce * _rollAmount * Time.fixedDeltaTime);
            _rigidBody.AddTorque(transform.forward * (_rollForce * _rollAmount * Time.fixedDeltaTime ));
        }

        // Apply thrust force
        if (!Mathf.Approximately(0f, _thrustAmount))
        {
            //speedThrust += transform.forward * (_thrustForce * _thrustAmount * Time.fixedDeltaTime);
            //_rigidBody.AddForce(transform.forward * (_thrustForce * _thrustAmount * Time.fixedDeltaTime));
        }
        if(particleSystem != null)
        {
            // Mettez à jour la vitesse des particules basée sur la vitesse du Rigidbody
            Vector3 scaledVelocity = _rigidBody.velocity * -10;
            /// Appliquer la nouvelle vitesse au module velocity over lifetime
            //velocityModule.x = new ParticleSystem.MinMaxCurve(scaledVelocity.x);
            //velocityModule.y = new ParticleSystem.MinMaxCurve(scaledVelocity.y);
            //velocityModule.zMultiplier = scaledVelocity.z;//new ParticleSystem.MinMaxCurve(scaledVelocity.z ); //scaledVelocity.z + speedThrust.z
            velocityModule.speedModifier = new ParticleSystem.MinMaxCurve(-_thrustAmount);
        }



    }
}
