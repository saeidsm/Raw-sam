param(
 [Parameter(Mandatory=$true)][string]$Source,
 [Parameter(Mandatory=$true)][string]$Plan,
 [Parameter(Mandatory=$true)][string]$Output,
 [Parameter(Mandatory=$true)][string]$Audit
)
# Run with Windows PowerShell 5.1; PowerShell 7 COM optional arguments differ.
$ErrorActionPreference='Stop'
if(Test-Path -LiteralPath $Output){throw 'Output already exists'}
if(Test-Path -LiteralPath $Audit){throw 'Audit already exists'}
$planData=Get-Content -LiteralPath $Plan -Raw -Encoding UTF8 | ConvertFrom-Json
$changes=@($planData.changes)
if(!$changes.Count){throw 'Empty plan'}
if(@($changes.uid | Select-Object -Unique).Count -ne $changes.Count){throw 'Duplicate UID'}
foreach($c in $changes){
 foreach($key in @('uid','name','old','new')){if($null -eq $c.$key){throw "Missing plan field $key"}}
 if($c.uid -isnot [int] -and $c.uid -isnot [long]){throw 'UID must be an integer'}
 foreach($key in @('old','new')){
  if($c.$key -is [string] -or $c.$key -is [bool]){throw 'Quantity must be a JSON number'}
  $v=[double]$c.$key
  if([double]::IsNaN($v) -or [double]::IsInfinity($v) -or $v -lt 0){throw 'Invalid quantity'}
 }
}
$sourceHash=(Get-FileHash -LiteralPath $Source -Algorithm SHA256).Hash
$planHash=(Get-FileHash -LiteralPath $Plan -Algorithm SHA256).Hash
if(!$planData.sourceSha256 -or $sourceHash -ne $planData.sourceSha256){throw 'Missing or mismatched source hash'}
Copy-Item -LiteralPath $Source -Destination $Output
$app=New-Object -ComObject MSProject.Application
$app.DisplayAlerts=$false
$opened=$false
function Get-Structure($project) {
 $rows=@()
 foreach($task in $project.Tasks){
  if($null -eq $task){continue}
  $r=[ordered]@{uid=$task.UniqueID}
  foreach($key in @('ID','Name','OutlineLevel','Summary','Milestone','Start','Finish','Duration','PercentComplete','ActualStart','ActualFinish','BaselineStart','BaselineFinish','BaselineCost','Predecessors','Successors','Calendar','ConstraintType','ConstraintDate','Cost','Work','ResourceNames','Number9')){
   $r[$key]=[string]$task.$key
  }
  $rows+=$r
 }
 return ($rows | ConvertTo-Json -Depth 5 -Compress)
}
try {
 $app.FileOpenEx($Output,$false) | Out-Null
 $opened=$true
 $project=$app.ActiveProject
 $beforeStructure=Get-Structure $project
 $beforeSummary=$project.ProjectSummaryTask.Number7
 $beforeStatus=[string]$project.StatusDate
 $map=@{}
 foreach($t in $project.Tasks){if($null -ne $t){$map[[int]$t.UniqueID]=$t}}
 # Validate the entire plan before any write.
 foreach($c in $changes){
  $t=$map[[int]$c.uid]
  if($null -eq $t -or $t.Summary){throw "Unknown or summary UID $($c.uid)"}
  if($t.Name -ne $c.name){throw "Name guard mismatch UID $($c.uid)"}
  if([Math]::Abs($t.Number5-[double]$c.old) -gt 0.000001){throw "Old quantity mismatch UID $($c.uid)"}
  $q=[double]$c.new
  if([double]::IsNaN($q) -or [double]::IsInfinity($q) -or $q -lt 0){throw 'Invalid quantity'}
 }
 foreach($c in $changes){$map[[int]$c.uid].Number5=[double]$c.new}
 $app.CalculateProject() | Out-Null
 foreach($c in $changes){if([Math]::Abs($map[[int]$c.uid].Number5-[double]$c.new) -gt 0.000001){throw 'Write read-back failed'}}
 $app.FileSave() | Out-Null
 $app.FileCloseEx(0) | Out-Null
 $opened=$false
 $app.FileOpenEx($Output,$true) | Out-Null
 $opened=$true
 $afterStructure=Get-Structure $app.ActiveProject
 if($beforeStructure -ne $afterStructure){throw 'Unexpected schedule structure/date/cost/total change; inspect diagnostic copy before delivery'}
 if($beforeStatus -ne [string]$app.ActiveProject.StatusDate){throw 'Unexpected status date change'}
 $afterSummary=$app.ActiveProject.ProjectSummaryTask.Number7
 $fields=@()
 foreach($i in 1..20){$id=$app.FieldNameToFieldConstant("Number$i",0);$fields+=@{name="Number$i";id=$id;formula=$app.CustomFieldGetFormula($id)}}
 $rows=@()
 foreach($t in $app.ActiveProject.Tasks){
  if($null -eq $t){continue}
  $r=@{uid=$t.UniqueID;id=$t.ID;name=$t.Name;summary=$t.Summary}
  foreach($i in 1..20){$r["Number$i"]=$t."Number$i"}
  foreach($i in 1..5){$r["OutlineCode$i"]=$t."OutlineCode$i"}
  $rows+=$r
 }
 $byUid=@{};foreach($r in $rows){$byUid[[int]$r.uid]=$r}
 foreach($c in $changes){if([Math]::Abs($byUid[[int]$c.uid].Number5-[double]$c.new) -gt 0.000001){throw 'Reopened quantity mismatch'}}
 if((Get-FileHash -LiteralPath $Source -Algorithm SHA256).Hash -ne $sourceHash){throw 'Original source changed'}
 @{file=$Output;sourceSha256=$sourceHash;planSha256=$planHash;fields=$fields;tasks=$rows;applied=$changes.Count;reopened=$true;structurePreserved=$true;statusDate=$beforeStatus;summaryBefore=$beforeSummary;summaryAfter=$afterSummary} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $Audit -Encoding UTF8
 Write-Output "Saved and reopened $($changes.Count) quantity changes: $Output"
} finally {
 if($opened){$app.FileCloseEx(0) | Out-Null}
 # Do not quit a shared Project application or close other documents.
}
