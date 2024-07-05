using System.Collections;
using System.Collections.Generic;
using OVR.OpenVR;
using TMPro;
using UnityEngine;

public class CalibrationProcess : MonoBehaviour
{

    private int pointCount = 0;
    private Vector3 p1 = Vector3.zero;
    private Vector3 p2 = Vector3.zero;
    private Vector3 p3 = Vector3.zero;
    private Vector3 normal = Vector3.zero;

    [SerializeField] private GameObject plane;

    [SerializeField] private Transform leftHand;
    [SerializeField] private Transform rightHand;

    // [SerializeField] private canvas calibrationButton
    [SerializeField] private TextMeshProUGUI p1AreaText;
    [SerializeField] private TextMeshProUGUI p2AreaText;
    [SerializeField] private TextMeshProUGUI p3AreaText;
    [SerializeField] private TextMeshProUGUI normalAreaText;

    public void StartCallibration()
    {
        ResetPoints();
        //button color : green
    }

    private void ResetPoints()
    {
        pointCount = 0;
        p1AreaText.text = string.Empty;
        p2AreaText.text = string.Empty;
        p3AreaText.text = string.Empty;
        normalAreaText.text = string.Empty;
    }

    private void EndCalibration()
    {
        CalculateNormal();
        plane.transform.position = p1;
        if(Vector3.Dot(normal, leftHand.transform.position - p1) > 0) 
            plane.transform.up = normal;
        else plane.transform.up = -normal;


        //button color : white
    }

    public void AddPoint()
    {
        pointCount++;
        switch(pointCount)
        {
            case 1:
                p1 = GetPoint();
                p1AreaText.text = p1.ToString();
                break;
            case 2:
                p2 = GetPoint();
                p2AreaText.text = p2.ToString();
                break;
            case 3:
                p3 = GetPoint();
                p3AreaText.text = p3.ToString();
                EndCalibration();
                break;
            default:
                pointCount = 3;
                break;
        }
    }

    private Vector3 GetPoint()
    {
        return rightHand.position;
    }

    private void CalculateNormal()
    {
        normal = (Vector3.Cross(p2 - p1, p3 - p1)).normalized;
        normalAreaText.text = normal.ToString();
    }
}
