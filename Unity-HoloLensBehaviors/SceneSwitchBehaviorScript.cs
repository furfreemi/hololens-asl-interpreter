using UnityEngine;
using UnityEngine.VR.WSA.Input;
using System.Collections;
using UnityEngine.SceneManagement;

public class SceneSwitchBehaviorScript : MonoBehaviour
{
    string nextScene = "school";
    GestureRecognizer recognizer;
    public static SceneSwitchBehaviorScript Instance { get; private set; }

    void Start()
    {
        Instance = this;
        recognizer = new GestureRecognizer();
        recognizer.TappedEvent += (source, tapCount, ray) =>
        {
            SceneManager.LoadScene(nextScene);
        };

        recognizer.StartCapturingGestures();
    }

    void Update()
    {

    }
}
