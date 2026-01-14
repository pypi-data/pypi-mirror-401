from geoexpress.core.encoder import encode


def batch_encode(jobs: list[dict], progress_cb=None):
    total = len(jobs)
    results = []

    for i, job in enumerate(jobs, start=1):
        if progress_cb:
            progress_cb(i, total, job)

        try:
            out = encode(
                job["input"],
                job["output"],
                job.get("options")
            )
            results.append({"job": job, "status": "success", "output": out})
        except Exception as e:
            results.append({"job": job, "status": "failed", "error": str(e)})

    return results
