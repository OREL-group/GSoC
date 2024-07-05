using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
[RequireComponent(typeof(Skybox))]
public class SkyBoxSetter : MonoBehaviour
{
    [SerializeField] List<Material> _skyBoxMaterials;
    Skybox _skybox;
    // Start is called before the first frame update
    void Start()
    {
        
    }
    // Update is called once per frame
    void Update()
    {
        
    }

    private void Awake()
    {
        _skybox = GetComponent<Skybox>();
    }
    private void OnEnable()
    {
        changeSkybox(0);
    }

    private void changeSkybox(int skyBox)
    {
        if(_skybox != null && skyBox >= 0 && skyBox<= _skyBoxMaterials.Count)
        {
            _skybox.material = _skyBoxMaterials[skyBox];
        }
    }
}
